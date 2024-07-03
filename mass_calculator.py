import re

# Detailed dictionary including isotopes for hydrogen, oxygen, nitrogen, and carbon
isotope_data = {
    'H': {
        'H-1': {'mass': 1.00782503223, 'abundance': 0.999885},
        'H-2': {'mass': 2.01410177812, 'abundance': 0.000115},
        'H-3': {'mass': 3.0160492779, 'abundance': 0.0},  # Tritium is very rare
    },
    'C': {
        'C-12': {'mass': 12.0, 'abundance': 0.9893},
        'C-13': {'mass': 13.00335483507, 'abundance': 0.0107},
        'C-14': {'mass': 14.0032419884, 'abundance': 0.0},  # C-14 is very rare and radioactive
    },
    'N': {
        'N-14': {'mass': 14.00307400443, 'abundance': 0.99636},
        'N-15': {'mass': 15.00010889888, 'abundance': 0.00364},
    },
    'O': {
        'O-16': {'mass': 15.99491461957, 'abundance': 0.99757},
        'O-17': {'mass': 16.99913175650, 'abundance': 0.00038},
        'O-18': {'mass': 17.99915961286, 'abundance': 0.00205},
    },
    # Add more elements and isotopes as needed
}

proton_mass = 1.007276466812  # Mass of a proton
electron_mass = 0.00054857990924  # Mass of an electron

# Function to parse chemical formula including isotopes
def parse_formula(formula):
    try:
        # Regex to match elements with optional isotopes in brackets and optional counts
        elements = re.findall(r'(\[?\d*\]?[A-Z][a-z]?)(\d*)', formula)
        composition = {}
        for (element, count) in elements:
            count = int(count) if count else 1
            if element.startswith('['):
                # Isotope specific
                element_key = element
                element_symbol = re.findall(r'\[(\d+)\]([A-Z][a-z]?)', element)[0][1]
                isotope_key = f"{element_symbol}-{element.split('[')[1].split(']')[0]}"
            else:
                # Default to most abundant isotope
                element_key = select_isotope(element)
                isotope_key = element_key
            if isotope_key in composition:
                composition[isotope_key] += count
            else:
                composition[isotope_key] = count
        return composition
    except Exception as e:
        raise ValueError(f"Error parsing formula: {e}")

# Function to select the most abundant isotope
def select_isotope(element):
    try:
        isotopes = isotope_data[element]
        return max(isotopes, key=lambda k: isotopes[k]['abundance'])
    except KeyError:
        raise ValueError(f"Element {element} is not recognized or has no isotopes defined.")

# Function to calculate exact mass
def calculate_exact_mass(formula):
    try:
        composition = parse_formula(formula)
        exact_mass = 0.0
        for isotope, count in composition.items():
            element = isotope.split('-')[0]
            exact_mass += isotope_data[element][isotope]['mass'] * count
        return exact_mass
    except Exception as e:
        raise ValueError(f"Error calculating exact mass: {e}")

# Function to calculate M+H
def calculate_m_plus_h(formula):
    try:
        exact_mass = calculate_exact_mass(formula)
        return exact_mass + proton_mass - electron_mass
    except Exception as e:
        raise ValueError(f"Error calculating M+H: {e}")

# Function to calculate M-H
def calculate_m_minus_h(formula):
    try:
        exact_mass = calculate_exact_mass(formula)
        return exact_mass - proton_mass + electron_mass
    except Exception as e:
        raise ValueError(f"Error calculating M-H: {e}")

# Function to dynamically input formula and calculate masses
def calculate_masses():
    while True:
        try:
            formula = input("Enter the chemical formula: ").strip()
            exact_mass = round(calculate_exact_mass(formula), 5)
            m_plus_h = round(calculate_m_plus_h(formula), 5)
            m_minus_h = round(calculate_m_minus_h(formula), 5)

            print(f"\nResults for {formula}:")
            print(f"Exact Mass: {exact_mass:.5f}")
            print(f"M+H: {m_plus_h:.5f}")
            print(f"M-H: {m_minus_h:.5f}")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please try again.")
    
    input("\nPress Enter to exit...")

# Run the dynamic input function
calculate_masses()
