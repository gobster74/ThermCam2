#################
# Contains the spec





#ip = "opc.tcp://169.254.243.7:5000"
ip = "opc.tcp://10.35.128.20:50000"
current_layer = 'ns=2;s=Scan System."Scan System.Current Layer"'
job_file = 'ns=2;s=Scan System."Scan System.JobFile"'	
scan_status = 'ns=2;s=Scan System."Scan System.Status"'
scan_command ='ns=2;s=Scan System."Scan System.Command"'
#############SF0################
SF0_Field_Command = 'ns=2;s=Scan System.Scan Field 0."Scan Field 0.Command"'
SF0_Field_x_Feedback = 'ns=2;s=Scan System.Scan Field 0."Scan Field 0.X Feedback"'
SF0_Field_x_Request = 'ns=2;s=Scan System.Scan Field 0."Scan Field 0.X Request"'
SF0_Field_y_Feedback = 'ns=2;s=Scan System.Scan Field 0."Scan Field 0.Y Feedback"'
SF0_Field_y_Request = 'ns=2;s=Scan System.Scan Field 0."Scan Field 0.Y Request"'
SF0_Field_V_Feedback = 'ns=2;s=Scan System.Scan Field 0."Scan Field 0.V Feedback"'
SF0_Field_V_Request = 'ns=2;s=Scan System.Scan Field 0."Scan Field 0.V Request"'
SF0_Field_DataBlockInfo = 'ns=2;s=Scan System.Scan Field 0."Scan Field 0.Datablock Info"'

############SF0Laser############
SF0_Laser_Diameter_Feedback = 'ns=2;s=Scan System.Scan Field 0.Laser 0."Laser 0.Diameter Feedback"'
SF0_Laser_Diameter_Request = 'ns=2;s=Scan System.Scan Field 0.Laser 0."Laser 0.Diameter Request"'
SF0_Laser_Power_Feedback = 'ns=2;s=Scan System.Scan Field 0.Laser 0."Laser 0.Power Feedback"'
SF0_Laser_Power_Request = 'ns=2;s=Scan System.Scan Field 0.Laser 0."Laser 0.Power Request"'
SF0_Laser_Control_Feedback = 'ns=2;s=Scan System.Scan Field 0.Laser 0."Laser 0.Control Feedback"'
SF0_Laser_Control_Request = 'ns=2;s=Scan System.Scan Field 0.Laser 0."Laser 0.Control Request"'
#############SF1################
SF1_Field_Command = 'ns=2;s=Scan System.Scan Field 1."Scan Field 1.Command"'
SF1_Field_x_Feedback = 'ns=2;s=Scan System.Scan Field 1."Scan Field 1.X Feedback"'
SF1_Field_x_Request = 'ns=2;s=Scan System.Scan Field 1."Scan Field 1.X Request"'
SF1_Field_y_Feedback = 'ns=2;s=Scan System.Scan Field 1."Scan Field 1.Y Feedback"'
SF1_Field_y_Request = 'ns=2;s=Scan System.Scan Field 1."Scan Field 1.Y Request"'
SF1_Field_V_Feedback = 'ns=2;s=Scan System.Scan Field 1."Scan Field 1.V Feedback"'
SF1_Field_V_Request = 'ns=2;s=Scan System.Scan Field 1."Scan Field 1.V Request"'
############SF1Laser############
SF1_Laser_Diameter_Feedback = 'ns=2;s=Scan System.Scan Field 1.Laser 1."Laser 1.Diameter Feedback"'
SF1_Laser_Diameter_Request = 'ns=2;s=Scan System.Scan Field 1.Laser 1."Laser 1.Diameter Request"'
SF1_Laser_Power_Feedback = 'ns=2;s=Scan System.Scan Field 1.Laser 1."Laser 1.Power Feedback"'
SF1_Laser_Power_Request = 'ns=2;s=Scan System.Scan Field 1.Laser 1."Laser 1.Power Request"'
SF1_Laser_Control_Feedback = 'ns=2;s=Scan System.Scan Field 1.Laser 1."Laser 1.Control Feedback"'
SF1_Laser_Control_Request = 'ns=2;s=Scan System.Scan Field 1.Laser 1."Laser 1.Control Request"'




#Laser Parameters
min_power = 60
min_diameter = 0.05
max_power = 280
max_diameter = 0.5
nominal_velocity = 1000

#BasePlate 

BP_Size = [150,150]
SF0_Center = [20,0]
import asyncio
from asyncua import Client

async def list_all_nodes(url, output_file):
    async with Client(url) as client:
        root = client.get_root_node()
        
        async def recursive_node_browse(node, file_handle, level=0):
            indent = "  " * level
            node_id = node.nodeid
            node_name = await node.read_display_name()
            file_handle.write(f"{indent}Node ID: {node_id}, Name: {node_name.Text}\n")

            try:
                children = await node.get_children()
                for child in children:
                    await recursive_node_browse(child, file_handle, level + 1)
            except Exception as e:
                file_handle.write(f"{indent}Error browsing node: {e}\n")

        with open(output_file, 'w') as f:
            await recursive_node_browse(root, f)

if __name__ == "__main__":
    server_url = ip  # Replace with your OPC UA server URL
    output_file = "opcua_nodes.txt"  # Output file name
    asyncio.run(list_all_nodes(server_url, output_file))