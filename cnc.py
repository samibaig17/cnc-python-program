import sys
import ezdxf
import math

def ReadDxfFile():
    """
    Prompts the user to provide a .dxf file name from the command line.
    
    Returns:
        str: The name of the .dxf file provided by the user.
    """
    # Check if the user provided a command line argument
    if len(sys.argv) < 2:
        print("Usage: python script.py <filename.dxf>")
        sys.exit(1)  # Exit the program if no file is provided
    
    # Get the file name from the command line arguments
    file_name = sys.argv[1]
    
    # Check if the file has a .dxf extension
    if not file_name.lower().endswith('.dxf'):
        print("Error: The file must be in .dxf format.")
        sys.exit(1)  # Exit if the file format is incorrect
    
    return file_name

def calculate_area_of_all_entities(entity):
    """
    Calculates the area of a given entity.
    
    Args:
        entity: The DXF entity for which to calculate the area.
    
    Returns:
        float: The area of the entity in square units.
    """
    if entity.dxftype() == 'LWPOLYLINE':
        return entity.area
    elif entity.dxftype() == 'POLYLINE':
        return entity.area
    elif entity.dxftype() == 'CIRCLE':
        radius = entity.dxf.radius
        return math.pi * (radius ** 2)  # Area of a circle
    elif entity.dxftype() == 'ARC':
        radius = entity.dxf.radius
        angle = entity.dxf.end_angle - entity.dxf.start_angle
        return (angle / 360) * (math.pi * (radius ** 2))  # Area of the arc sector
    return 0.0

def calculate_total_area(dxf_file):
    """
    Calculates the total area of all relevant entities defined in the provided .dxf file.
    
    Args:
        dxf_file (str): The name of the .dxf file to process.
    
    Returns:
        float: The total area of the entities in square units.
    """
    total_area = 0.0
    
    # Load the DXF file
    doc = ezdxf.readfile(dxf_file)
    msp = doc.modelspace()
    
    # Iterate through all entities in the model space
    for entity in msp:
        area = calculate_area_of_all_entities(entity)
        total_area += area

    return total_area

def calculate_quantity_of_entities(dxf_file):
    """
    Calculates the quantity of specific entities defined in the provided .dxf file.
    
    Args:
        dxf_file (str): The name of the .dxf file to process.
    
    Returns:
        dict: A dictionary containing the counts of different entity types.
    """
    # Initialize a dictionary to hold the counts of each entity type
    quantity = {
        'LINE': 0,
        'LWPOLYLINE': 0,
        'POLYLINE': 0,
        'CIRCLE': 0,
        'ARC': 0,
        'TEXT': 0,
        'MTEXT': 0,
        # Add more entity types as needed
    }
    
    # Load the DXF file
    doc = ezdxf.readfile(dxf_file)
    msp = doc.modelspace()
    
    # Iterate through all entities in the model space
    for entity in msp:
        entity_type = entity.dxftype()
        if entity_type in quantity:
            quantity[entity_type] += 1

    return quantity

def calculate_object_thickness(dxf_file):
    """
    Calculates the thickness of the object defined in the provided .dxf file.
    
    Args:
        dxf_file (str): The name of the .dxf file to process.
    
    Returns:
        float: The calculated thickness of the object in the same units as the DXF file.
    """
    # Initialize variables to track the minimum and maximum y-coordinates
    min_y = float('inf')
    max_y = float('-inf')
    
    # Load the DXF file
    doc = ezdxf.readfile(dxf_file)
    msp = doc.modelspace()
    
    # Iterate through all LINE, LWPOLYLINE, POLYLINE, CIRCLE, and ARC entities
    for entity in msp:
        if entity.dxftype() == 'LINE':
            # For lines, get the start and end points
            min_y = min(min_y, entity.dxf.start.y, entity.dxf.end.y)
            max_y = max(max_y, entity.dxf.start.y, entity.dxf.end.y)
        elif entity.dxftype() in ('LWPOLYLINE', 'POLYLINE'):
            # For polylines, iterate through vertices
            for vertex in entity.vertices():
                min_y = min(min_y, vertex.y)
                max_y = max(max_y, vertex.y)
        elif entity.dxftype() == 'CIRCLE':
            # For circles, calculate the topmost and bottommost points
            min_y = min(min_y, entity.dxf.center.y - entity.dxf.radius)
            max_y = max(max_y, entity.dxf.center.y + entity.dxf.radius)
        elif entity.dxftype() == 'ARC':
            # For arcs, calculate the topmost and bottommost points
            min_y = min(min_y, entity.dxf.center.y - entity.dxf.radius)
            max_y = max(max_y, entity.dxf.center.y + entity.dxf.radius)

    # Calculate the thickness
    if min_y == float('inf') or max_y == float('-inf'):
        return 0.0  # No valid entities found

    thickness = max_y - min_y
    return thickness

def calculate_object_width(dxf_file):
    """
    Calculates the width of the object defined in the provided .dxf file.
    
    Args:
        dxf_file (str): The name of the .dxf file to process.
    
    Returns:
        float: The calculated width of the object in the same units as the DXF file.
    """
    # Initialize variables to track the minimum and maximum x-coordinates
    min_x = float('inf')
    max_x = float('-inf')
    
    # Load the DXF file
    doc = ezdxf.readfile(dxf_file)
    msp = doc.modelspace()
    
    # Iterate through all LINE, LWPOLYLINE, POLYLINE, and CIRCLE entities
    for entity in msp:
        if entity.dxftype() == 'LINE':
            # For lines, get the start and end points
            min_x = min(min_x, entity.dxf.start.x, entity.dxf.end.x)
            max_x = max(max_x, entity.dxf.start.x, entity.dxf.end.x)
        elif entity.dxftype() in ('LWPOLYLINE', 'POLYLINE'):
            # For polylines, iterate through vertices
            for vertex in entity.vertices():
                min_x = min(min_x, vertex.x)
                max_x = max(max_x, vertex.x)
        elif entity.dxftype() == 'CIRCLE':
            # For circles, calculate the leftmost and rightmost points
            min_x = min(min_x, entity.dxf.center.x - entity.dxf.radius)
            max_x = max(max_x, entity.dxf.center.x + entity.dxf.radius)
        elif entity.dxftype() == 'ARC':
            # For arcs, calculate the leftmost and rightmost points
            min_x = min(min_x, entity.dxf.center.x - entity.dxf.radius)
            max_x = max(max_x, entity.dxf.center.x + entity.dxf.radius)

    # Calculate the width
    if min_x == float('inf') or max_x == float('-inf'):
        return 0.0  # No valid entities found

    width = max_x - min_x
    return width

def calculate_machine_cut_length(dxf_file):
    """
    Calculates the machine cut length based on the provided .dxf file.
    
    Args:
        dxf_file (str): The name of the .dxf file to process.
    
    Returns:
        float: The calculated machine cut length in meters.
    """
    # Initialize total cut length
    total_length = 0.0
    
    # Load the DXF file
    doc = ezdxf.readfile(dxf_file)
    
    # Iterate through all LINE entities in the model space
    for line in doc.modelspace().query('LINE'):
        # Calculate the length of the line
        length = line.dxf.start.distance(line.dxf.end)
        total_length += length
    
    # Iterate through all POLYLINE entities
    for polyline in doc.modelspace().query('POLYLINE'):
        # Calculate the length of the polyline
        total_length += sum(segment.length for segment in polyline.vertices())
    
    # Iterate through all ARC entities
    for arc in doc.modelspace().query('ARC'):
        # Calculate the arc length: length = radius * angle (in radians)
        radius = arc.dxf.radius
        angle = arc.dxf.end_angle - arc.dxf.start_angle
        # Convert angle from degrees to radians
        angle_rad = math.radians(angle)
        arc_length = radius * angle_rad
        total_length += arc_length
    
    # Iterate through all CIRCLE entities
    for circle in doc.modelspace().query('CIRCLE'):
        # Calculate the circumference of the circle: C = 2 * π * r
        radius = circle.dxf.radius
        circumference = 2 * math.pi * radius
        total_length += circumference  # Add the full circumference for circles
    
    # Return the total cut length in meters
    return total_length

def calculate_weight(cut_length, width, thickness):
    """
    Calculates the weight of the design based on the machine cut length.
    
    Args:
        cut_length (float): The length of the cut in meters.
    
    Returns:
        float: The calculated weight of the design in kilograms.
    """
    # Define a constant for weight per meter (for example purposes)
    weight_per_meter = 2.5  # Assume 2.5 kg per meter of cut length
    
    # Calculate the total weight based on the cut length
    weight = cut_length * width * thickness
    
    return weight

def main():
    """
    Main function to execute the program logic.
    """
    # Read the DXF file name from command line
    dxf_file = ReadDxfFile()

    # Calculate the total area of all entities in the DXF file
    total_area = calculate_total_area(dxf_file)

    # Calculate the quantity of entities in the DXF file
    quantity = calculate_quantity_of_entities(dxf_file)
    print("Quantity of entities in the DXF file:")
    for entity_type, count in quantity.items():
        print(f"{entity_type}: {count}")

    # Calculate the object thickness from the DXF file
    calc_thickness = calculate_object_thickness(dxf_file)

    # Calculate the object width from the DXF file
    calc_width = calculate_object_width(dxf_file)

    # Calculate the machine cut length
    cut_length = calculate_machine_cut_length(dxf_file)
    
    # Calculate the weight of the design based on the cut length
    weight = calculate_weight(cut_length * 1000, calc_width, calc_thickness)  # Convert cut length to mm for weight calculation
    
    # Output the results
    print(f"Total area of all entities in the DXF file: {total_area:.2f} square units")
    print(f"Object Thickness: {calc_thickness} units")
    print(f"Object Width: {calc_width} units")
    print(f"Machine Cut Length: {cut_length} meters")
    print(f"Weight of the Design: {weight} kg")

# Entry point of the program
if __name__ == "__main__":
    main()
