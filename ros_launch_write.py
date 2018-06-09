#!/usr/bin/env python

class Group:
    def __init__(self):
        group = self
        group.nodes = []
	group.sub_groups = []

    def cmd_vel_mux(self):
        summary = ""
        overview = ""
        arguments = {
          "node_name": (type(""), "n_cmd_vel_mux", None, None,
          "The name of this node.")
        }
        package = "nodelet"
        executable = "nodelet"
    
        """
         <node machine="$(arg machine_name)" name="mobile_base_nodelet_manager"
          pkg="nodelet" type="nodelet" args="manager"/>
            
         <node  machine="$(arg machine_name)" name="cmd_vel_mux"
          pkg="nodelet" type="nodelet"
          args="load yocs_cmd_vel_mux/CmdVelMuxNodelet mobile_base_nodelet_manager">
            
          <param name="yaml_cfg_file" value="$(arg yaml_dir)/mux.yaml"/>
          <remap from="cmd_vel_mux/output" to="mobile_base/commands/velocity"/>
         </node>
        </launch>
            
        """
	node = Node(summary, overview, arguments, package, executable)
	group = self
	group.node_append(node)

    def group_append(self, group):
	assert isinstance(group, Group)
	group = self
	group.sub_groups.append(group)

    def joint_state_publisher(self, **kwargs):
	""" *Group*: Append a joint_state_publisher *Node* to the *Group* object (i.e. *self*):
	    *kwargs* is a standard Python keywords dictionary.
        """

	# Verify arguments:
	assert isinstance(kwargs, dict)

        summary = "Launches joint_state_publisher node."
        overview = "This will launch a joint_state_publisher node."
        arguments = {
          "joint_states_ptopic": (type(""), "joint_states", "joint_states", None,
            "The topic to publish joint states on."),
          "rate": (type(0), 10, None, "rate",
            "The rate (in Hertz) at which joint states are published."),
          "use_gui": (type(False), False, None, "use_gui",
            "If \"True\", pops up a GUI window that allows the joints to be changed.")
          }
        package = "$(arg jsp)"
        executable = "$(arg jsp)"
    
        #<param name="use_gui" value="$(arg use_gui)" />
        #<param name="rate" value="$(arg rate)" />
        #<remap from="joint_states" to="$(arg joint_states_ptopic)" />
    
        # <!--FIXME: Add the following parameters:
        # robot_description
        # dependent_joints
        # source_list
        # use_mimic_tags
        # zeros
        # use_smallest_joint_limits
        # publish_default_positions
        # publish_default_velocities
        # publish_default_efforts
        # -->
        
        node = \
          Node("n_joint_state_publisher", summary, overview, arguments, package, executable, kwargs)
	group = self
	group.node_append(node)
    
    def newer_xml_write(self):
	""" *Group*: Write out a newer XML file for the *Group* object (i.e. *self*.) """

	# Use *group* instead of *self*:
	group = self

	# Write out all of the *nodes* from *group*:
	nodes = group.nodes
	for node in nodes:
	    # Open *xml_file_name* and write *node* into it:
            xml_file_name = \
             "/home/wayne/catkin_ws/src/ubiquity_launches/{0}/launch/{0}.newer_launch.xml". \
             format(node.name)
	    #print("xml_file_name={0}".format(xml_file_name))
            with open(xml_file_name, "w") as xml_file:
                node.newer_xml_write("", xml_file)

	# Write all of the *sub_groups*
	sub_groups = group.sub_groups
	for group in sub_groups:
	    group.new_xml_write()

    def node_append(self, node):
	assert isinstance(node, Node)
	group = self
	group.nodes.append(node)

    def relay(self, **kwargs):
	# Verify argument types:
	assert isinstance(kwargs, dict)

        summary = "Relay messages from one topic to another."
        overview = """This launch file directory will start a node that
          runs the ROS [relay](http://wiki.ros.org/topic_tools/relay) node
          that forwards messages from one topic to another one."""
        arguments = {
          "in_topic": (type(""), None, None, None,
            "The input topic name."),
          "lazy": (type(False), False, None, "lazy",
            """ Set to `True` defer subscribing to the input topic until
            after there is at least one output topic; otherwise set to `False`
            to always subscribe to both topics."""),
          "out_topic": (type(""), None, None, None,
            "The output topic name."),
          "node_name": (type(""), "n_relay", None, None,
            "The name to assign to this node."),
          "unreliable": (type(False), False, None, "unreliable",
            """Set to `True` to negociate an unreliable connection
            for inbound data; other set to `False` for a reliable connection.""")
          }
        package = "topic_tools"
        executable = "relay"
        node = Node("n_relay",
	  summary, overview, arguments, package, executable, kwargs, output="screen")
	group = self
	group.node_append(node)
    
    def stage_ros(self, **kwargs):
	""" *Group*: Append a *Node* for a `stage_ros` node to the *Group* object (i.e. *self*.)
            *kwargs* is a Python keyword dictionary for specifying arguments.
	"""

	# Verify argument types:
	assert isinstance(kwargs, dict)
	print("kwargs=", kwargs)

	# Assemble the various arguments need for the *Node* initializer:
        summary = "Launches stage robot simulation envirnoment for ROS."
        overview = """ Stage is an environment for simulating robot operating
          in a simulated 2D environment.  This node starts up the ROS
          [stage_ros](http://wiki.ros.org/stage_ros) node to perform this simulation.
          The
          [Stage Manual](http://playerstage.sourceforge.net/doc/Stage-3.2.1/modules.html)
          is available elsewhere on the net."""
        arguments = {
            "base_scan_ptopic":
              (type(""), "base_scan", "base_scan", None,
              "Laser scan information is published to this topic."),
            "base_watchdog_timeout":
              (type(1.0), "0.2", None, "base_watchdog_timeout",
              """The time in seconds after receiving the last command on
                 the `cmd_vel` topic before the robot stops."""),
            "base_pose_ground_truth_ptopic":
              (type(""), "base_pose_ground_truth", "base_pose_ground_truth", None,
              "Ground truth pose information is publishde to this topic."),
            "camera_info_ptopic":
              (type(""), "camera_info", "camera_info", None,
              "Camera calibration information is published to this topic."),
            "cmd_vel_stopic":
              (type(""), "cmd_vel", "cmd_vel", None,
              "The velocity command to drive the roboto position in the model."),
            #"depth_ptopic":
            #  (type(""), "depth", "depth", None,
            #  "A depth camera image is published to this topic."),
            "image_ptopic":
              (type(""), "image", "image", None,
              "A visual camera imageis published to this topic."),
            "is_depth_canonical":
              (type(True), "true", None, "is_depth_canonical",
              """Specifies whether image depth should use a canonical
                 (32FC1) or OpenNI (16UC1) representation."""),
            "odom_ptopic":
              (type(""), "odom", "odom", None,
              "Odometry from the position model is published to this topic."),
            "rate":
              (type(10), "10", None, None,
              "The rate at which joint states are published."),
            "use_gui":
              (type(False), False, None, None,
              "If \"True\", pops up a GUI window that allows the joints to be changed."),
            "world_file":
              (type(""), None, None, None,
              """The `.world` file to construct the robot simulation environment.
                 Note that the currently the world file must be in a in a directory called
                 `.../maps/stage/` which need a bunch of .png files, .yaml files, etc.
                 Good luck finding any useful documentation.""")
            }
        package = "stage_ros"
        executable = "stageros"

	# Create the *Node* and append it to *group* (i.e. *self*):
	node = Node("n_stage_ros", summary, overview, arguments, package, executable, kwargs)
	group = self
        group.node_append(node)

    def xml_write(self):
	""" *Group*: Write out the XML for the *Group* object (i.e. *self*.) """

	# Use *group* instead of *self*:
	group = self

	# Write out each *node* from the *group* *nodes*:
	nodes = group.nodes
	for node in nodes:
	    # Open *xml_file_name* and write the XML for *node* into it:
            xml_file_name = \
             "/home/wayne/catkin_ws/src/ubiquity_launches/{0}/launch/{0}.new_launch.xml". \
             format(node.name)
	    #print("xml_file_name={0}".format(xml_file_name))
            with open(xml_file_name, "w") as xml_file:
                node.xml_write("", xml_file)

	# Write out each *sub_group* from the *sub_groups* of *group*:
	sub_groups = group.sub_groups
	for sub_group in sub_groups:
	    sub_group.xml_write()

class Node:
    # Tuple offsets:
    TYPE = 0
    DEFAULT = 1
    REMAP = 2
    PARAMETER = 3
    COMMENT = 4

    def __init__(self, name, summary, overview, arguments, package, executable, kwargs,
      output=None):
	""" *Node*: Initialize the *Node* object (i.e. *self*) to contain *name*, *summary*,
	    *overview*, *arguments*, *package*, *executable*, and *output*, where:
            
	    * *name*:       *name* specifies is the node name as a string,
	    * *summary*:    *summary* is a one line string that summarizes what the *node* does,
	    * *overview*:   *overview* is a string ('\n' characters are allowed for line breaks)
                            that provides a more detailed overview of what the *node* does,
            * *arguments*:  *arguments* is a Python dictionary object that where each key is the
	                    argument name string and the value is 5-tuple that provides information
	                    about the argument.  The 5-tuple is (*type*, *default*, *remap*,
                            *param*, comment*) where:

		            * *type* is the type of argument,
			    * *default* is either *None* (for a required argument) or
                              a non-*None* for an optional argument,
                            * remap* is either *None* (no remapping) or a string
                              (for <remap ... />),
                            * *param* is  either *None* (no parameter) or a string
                               (for <param ... />), and
	                    * *comment* is a string (i.e. embedded '\n' allowed) that
	                       describes what the argument is used for.
	    * *package*:    * *package* specifies the ROS package name (as a string) that
                              contains the executable, and
	    * *executable*: * *executable* specifies the executable name (as a string)
                              within the package.
            * *kwargs*:     * *kwargs* is a dictionary that contains specified arguments.
	"""

        # Verify argument types:
        assert isinstance(name, str) and name != ""
        assert isinstance(summary, str)
        assert isinstance(overview, str)
        assert isinstance(arguments, dict)
        assert isinstance(package, str)
        assert isinstance(executable, str)
	assert isinstance(kwargs, dict)
        assert isinstance(output, str) or output == None
        for argument_name, argument_tuple in arguments.iteritems():
            assert isinstance(argument_name, str) and argument_name != "" and \
              isinstance(argument_tuple, tuple) and len(argument_tuple) == 5, \
              "Argument '{0}' has length of {1}".format(argument_name, len(argument_tuple))

        arguments["node_name"] = (type(""), name, None, None, "The name to assign to this node.")

        # Load arguments into *Node* object (i.e. *self*):
        node = self
        node.name = name
        node.summary = summary
        node.overview = overview
        node.arguments = arguments
        node.package = package
        node.executable = executable
	node.kwargs = kwargs
        node.output = output

    def newer_xml_write(self, indent, xml_file):
	""" *Node*: ... """

        # Verify argument types:
        assert isinstance(indent, str)
        assert isinstance(xml_file, file)

        # Extract and sort *named_tuples* from *arguments*:
        node = self
	kwargs = node.kwargs
	assert isinstance(kwargs, dict)
        arguments = node.arguments
        named_tuples = node.arguments.items()
        named_tuples.sort(key=lambda named_tuple: named_tuple[0])

        # Construct the output file as a series of *lines*, starting with the header:
        lines = []
        lines.append("<launch>")        

	# Verify that each argument in *kwargs* actually exists in *arguments*
        # and has the correct type:
	for argument_name, argument_value in kwargs.iteritems():
	    assert argument_name in arguments
	    argument_tuple = arguments[argument_name]
	    argument_type = argument_tuple[Node.TYPE]
	    assert type(argument_value) == argument_type
        
        # Verify that the required arguments are present in *kwargs*:
        executable_arguments = []
        for argument_name, argument_tuple in named_tuples:
            argument_default = argument_tuple[Node.DEFAULT]
            argument_comment = argument_tuple[Node.COMMENT]
            if argument_default == None:
		#assert argument_name in kwargs, \
		if argument_name in kwargs:
                    executable_arguments.append(kwargs[argument_name])
		else:
                    print("Argument '{0}' not specified for node '{1}'".
                      format(argument_name, node.name))

        # Output `<node>` ... `</node>`:
        node_output = node.output
        output = "" if node_output == None else " output=\"{0}\" ".format(node_output)
        lines.append("  <node name=\"{0}\" pkg=\"{1}\" type=\"{2}\"{3}".
          format(node.name, node.package, node.executable, output))
        lines.append("   args=\"{0}\" >".format(' '.join(executable_arguments)))
        for argument_name, argument_tuple in named_tuples:
	    assert isinstance(argument_tuple, tuple) and len(argument_tuple) == 5
	    argument_default   = argument_tuple[Node.DEFAULT]
            argument_remap     = argument_tuple[Node.REMAP]
            argument_parameter = argument_tuple[Node.PARAMETER]
	    if argument_name in kwargs:
                argument_default = kwargs[argument_name]
	    print("argument_name={0} argument_tuple[0:4]={1} argument_default={2}".
	      format(argument_name, argument_tuple[0:4], argument_default))
            if argument_remap != None:
                lines.append("    <remap from=\"{0}\" to=\"{1}\" />".
                  format(argument_remap, argument_default))
            elif argument_parameter != None:
                lines.append("    <param name=\"{0}\" value=\"{1}\" />".
                  format(argument_parameter, argument_default))
        lines.append("  </node>")

        # Wrap up `</launch>`, compute a single *text* string, and write it out to *xml_file*:
        lines.append("</launch>")
        text = (indent + "\n").join(lines)
        xml_file.write(text)
        xml_file.write("\n")

    def xml_write(self, indent, xml_file):
	""" *Node*: ... """

        # Verify argument types:
        assert isinstance(indent, str)
        assert isinstance(xml_file, file)

        # Extract and sort *named_tuples* from *arguments*:
        node = self
        arguments = node.arguments
        named_tuples = node.arguments.items()
        named_tuples.sort(key=lambda named_tuple: named_tuple[0])

        # Construct the output file as a series of *lines*, starting with the header:
        lines = []
        lines.append("<launch>")        
        Node.argument_comment_append(lines, " ", "Summary", node.summary)
        Node.argument_comment_append(lines, " ", "Overview", node.overview)
        lines.append("")

        # Output the standard required arguments:
        lines.append(" <!-- Required Arguments: -->")
        lines.append(" <arg name=\"robot_platform\" />")
        lines.append("   <!--robot_platform: " +
          "The robot platform (e.g. \"magni\", \"loki\", etc.) -->")
        lines.append(" <arg name=\"robot_dir\" />")
        lines.append("   <!--robot_dir: The robot launch files and parameters directory. -->")
        lines.append(" <arg name=\"machine_name\" default=\"robot\"/>")
        lines.append("   <!--machine_name: The machine name (i.e. \"robot\" or \"viewer\") -->")
        lines.append(" <arg name=\"machine_host\" />")
        lines.append("   <!--machine_host: The DNS machine name (e.g. \"ubuntu.local\") -->")
        lines.append(" <arg name=\"machine_user\" />")
        lines.append("   <!--machine_user: The user account on the machine. -->")
        
        # Output the node specific required arguments:
        executable_arguments = []
        for argument_name, argument_tuple in named_tuples:
            argument_default = argument_tuple[Node.DEFAULT]
            argument_comment = argument_tuple[Node.COMMENT]
            if argument_default == None:
                lines.append(" <arg name=\"{0}\" />".format(argument_name, ))
                Node.argument_comment_append(lines, "   ", argument_name, argument_comment)
                executable_arguments.append("$(arg {0})".format(argument_name))
        lines.append("")

        lines.append(" <!-- Convenience arguments: -->")
        lines.append("")

        # Output the node specific optional arguments:
        lines.append(" <!-- Optional Arguments: -->")
        for argument_name, argument_tuple in named_tuples:
            argument_default = argument_tuple[Node.DEFAULT]
            argument_comment = argument_tuple[Node.COMMENT]
            if argument_default != None:
                lines.append(" <arg name=\"{0}\" default=\"{1}\" />".
                 format(argument_name, argument_default))
                Node.argument_comment_append(lines, "   ", argument_name, argument_comment)
        lines.append("")

        # Output `<machine ... />`:
        lines.append(" <!-- Machine configuration: -->")
        lines.append(" <machine name=\"$(arg machine_name)\"")
        lines.append("  address=\"$(arg machine_host)\" user=\"$(arg machine_user)\"")
        lines.append("  env-loader=\"/tmp/env_loader.sh\" />")
        lines.append("")

        # Output `<node>` ... `</node>`:
        lines.append(" <node machine=\"{0}\" name=\"{1}\"".
         format("$(arg machine_name)", "$(arg node_name)"))
        node_output = node.output
        output = "" if node_output == None else "output=\"{0}\" ".format(node_output)
        lines.append("  pkg=\"{0}\" type=\"{1}\" args=\"{2}\" {3}>".
         format(node.package, node.executable, ' '.join(executable_arguments), output))
        for argument_name, argument_tuple in named_tuples:
            argument_remap = argument_tuple[Node.REMAP]
            argument_parameter = argument_tuple[Node.PARAMETER]
            if argument_remap != None:
                lines.append("  <remap from=\"{0}\" to=\"$(arg {1})\" />".
                  format(argument_remap, argument_name))
            elif argument_parameter != None:
                lines.append("  <param name=\"{0}\" value=\"$(arg {1})\" />".
                  format(argument_parameter, argument_name))
        lines.append(" </node>")

        # Wrap up `</launch>`, compute a single *text* string, and write it out to *xml_file*:
        lines.append("</launch>")
        text = (indent + "\n").join(lines)
        xml_file.write(text)
        xml_file.write("\n")

    @staticmethod
    def argument_comment_append(lines, indent, name, comment):
	""" *Node*: ... """

        # Verify argument types:
        assert isinstance(indent, str)
        assert isinstance(lines, list)
        assert isinstance(name, str)
        assert isinstance(comment, str)

        #print("comment=", comment)
        comment_lines = comment.split('\n')
        #print("comment_lines=", comment_lines)
        comment_lines = [ comment_line.strip() for comment_line in comment_lines ] 
        #print("stripped_comment_lines=", comment_lines)

        # Shove `<!--NAME:` in front of first comment line:
        comment_lines[0] = "{0}<!--{1}: {2}".format(indent, name, comment_lines[0])

        # Stuff *extra_indent* in front of each comment line except the first one:
        extra_indent = indent + "    "
        for index in range(1, len(comment_lines)):
            comment_lines[index] = extra_indent + comment_lines[index]

        # Tack ` -->` onto end of last comment line:
        comment_lines[-1] = comment_lines[-1] + " -->"
        #print("updated_comment_lines=", comment_lines)

        # Tack *comment_lines* onto *lines*:
        lines.extend(comment_lines)

class Platform:
    def __init__(self, name):
        assert isinstance(name, str) and name != ""
        platform = self
        platform.name = name

class Swarm:
    def __init__(self, name):
        assert isinstance(name, str) and name != ""
        swarm = self
        swarm.name = name
        swarm.nodes = []

def main():
    group = Group()
    #group.joint_state_publisher()
    #group.relay()
    ubiquity_launches = "/home/wayne/catkin/src/ubiquity_launches"
    group.stage_ros(
      base_pose_ground_truth_ptopic="base_pose_ground_truth",
      base_scan_ptopic="scan",
      base_watchdog_timeout=0.5,
      cmd_vel_stopic="/mobile_base/commands/velocity",
      odom_ptopic="odom",
      world_file="{0}/m_robot_base/maps/stage/maze.world".format(ubiquity_launches))
    group.xml_write()
    group.newer_xml_write()

if __name__ == "__main__":
    main()
