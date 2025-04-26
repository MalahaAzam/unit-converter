import streamlit as st
from pint import UnitRegistry

# initialize unit registry
ureg = UnitRegistry()

# define unit categories with user-friendly names
unit_categories = {
    'Length': {
        'Meter (m)': 'meter',
        'Kilometer (km)': 'kilometer',
        'Mile (mi)': 'mile',
        'Yard (yd)': 'yard',
        'Foot (ft)': 'foot',
        'Inch (in)': 'inch'
    },
    'Mass': {
        'Kilogram (kg)': 'kilogram',
        'Gram (g)': 'gram',
        'Pound (lb)': 'pound',
        'Ounce (oz)': 'ounce'
    },
    'Temperature': {
        'Celsius (°C)': 'degC',
        'Fahrenheit (°F)': 'degF',
        'Kelvin (K)': 'kelvin'
    },
    'Volume': {
        'Liter (L)': 'liter',
        'Milliliter (mL)': 'milliliter',
        'Gallon (gal)': 'gallon',
        'Quart (qt)': 'quart',
        'Pint (pt)': 'pint'
    },
    'Time': {
        'Second (s)': 'second',
        'Minute (min)': 'minute',
        'Hour (h)': 'hour',
        'Day (d)': 'day',
        'Week (wk)': 'week',
        'Month (mo)': 'month',
        'Year (yr)': 'year'
    },
    'Area': {
        'Square Meter (m²)': 'meter**2',
        'Hectare (ha)': 'hectare',
        'Acre (ac)': 'acre'
    },
    'Speed': {
        'Meter/Second (m/s)': 'meter/second',
        'Kilometer/Hour (km/h)': 'kilometer/hour',
        'Mile/Hour (mph)': 'mile/hour'
    }
}

# Function to convert units (handles temperature and invalid conversions)
def convert_units(value, from_unit, to_unit):
    try:
        # Temperature special case
        if from_unit in ['degC', 'degF', 'kelvin'] and to_unit in ['degC', 'degF', 'kelvin']:
            quantity = ureg.Quantity(value, ureg(from_unit))
            result = quantity.to(ureg(to_unit))
        else:
            quantity = value * ureg(from_unit)
            # check if dimensions match before converting
            if quantity.dimensionality != ureg(to_unit).dimensionality:
                return "incompatible"
            result = quantity.to(to_unit)

        return result.magnitude
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def main():
    st.set_page_config(page_title="Google Style Unit Converter", layout="wide")
    st.title("Unit Converter")
    st.write("Easily convert between different units of measurement!")
    st.write("Select a category and enter the value to convert.")

    # Select category
    category = st.selectbox("Select a category:", list(unit_categories.keys()))
    units_dict = unit_categories[category]
    unit_labels = list(units_dict.keys())

    # User input
    value = st.number_input("Enter the value to convert:", min_value=0.0, format="%.2f")
    from_label = st.selectbox("From unit:", unit_labels)
    to_label = st.selectbox("To unit:", unit_labels)

    from_unit = units_dict[from_label]
    to_unit = units_dict[to_label]

    # Convert button
    if st.button("Convert"):
        result = convert_units(value, from_unit, to_unit)
        if result == "incompatible":
            st.error(f"Cannot convert {from_label} to {to_label} because they are different types of units.")
        elif isinstance(result, (int, float)):
            st.success(f"{value} {from_label} = {result:.2f} {to_label}")
        else:
            st.error("Conversion failed. Please check the input values.")

    # Footer
    st.markdown("---")
    st.write("Made with ❤️ by Malaha using Python and Streamlit")

if __name__ == "__main__":
    main()
