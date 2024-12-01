# ==================
# SETUP & CONNECTION
# ==================

from sqlalchemy import create_engine, text
import pandas as pd

conn_url = "postgresql://postgres:123@localhost:5432/5310project"
engine = create_engine(conn_url)
connection = engine.connect()




# ================
# DATA PREPERATION
# ================

"""
Notice that the agency addresses are stored in a single column in
the csv file, need to separate them into street_address1, street_address2, 
city, state, and zip codes. 
We decide to directly modify the loaded data in python.
"""

data = pd.read_csv('/Users/yuqi/Downloads/final_dataset.csv')

if "agency_address" in data.columns:
    # split the whole address line
    address_parts = data["agency_address"].str.split(",", expand=True) 

    # street address 1
    data["street_name_1"] = address_parts[0].str.strip()
    # street address 2   
    data["street_name_2"] = address_parts[1].str.strip() if address_parts.shape[1] > 1 else None

    if address_parts.shape[1] > 2: # extract city, state, and zip code
        city_state_zip = address_parts[2].str.extract(r'(?P<city>[\w\s]+),?\s*(?P<state>[A-Z]{2})\s*(?P<zipcode>\d{5})?')
        data["city"] = city_state_zip["city"].str.strip()
        data["state"] = city_state_zip["state"].str.strip()
        data["zipcode"] = city_state_zip["zipcode"].str.strip()




# ==========================
# QUERIES FOR DATA IMPORTING
# ==========================


# property
stmt_property = text("""
    INSERT INTO property (
        property_id, price, bedroom_number, bathroom_number, price_per_unit, 
        living_space, land_space, land_space_unit, property_type, property_status
    ) VALUES (
        :property_id, :price, :bedroom_number, :bathroom_number, :price_per_unit, 
        :living_space, :land_space, :land_space_unit, :property_type, :property_status
    )
    ON CONFLICT DO NOTHING;
""")

for _, row in data.iterrows():
    if pd.notnull(row["price"]) and pd.notnull(row["property_type"]):
        params = {
            "property_id": int(row["property_id"]) if not pd.isnull(row["property_id"]) else None,
            "price": float(row["price"]) if not pd.isnull(row["price"]) else None,
            "bedroom_number": int(row["bedroom_number"]) if not pd.isnull(row["bedroom_number"]) else None,
            "bathroom_number": int(row["bathroom_number"]) if not pd.isnull(row["bathroom_number"]) else None,
            "price_per_unit": float(row["price_per_unit"]) if not pd.isnull(row["price_per_unit"]) else None,
            "living_space": float(row["living_space"]) if not pd.isnull(row["living_space"]) else None,
            "land_space": float(row["land_space"]) if not pd.isnull(row["land_space"]) else None,
            "land_space_unit": row["land_space_unit"] if not pd.isnull(row["land_space_unit"]) else None,
            "property_type": row["property_type"],
            "property_status": row["property_status"] if not pd.isnull(row["property_status"]) else None
        }
        connection.execute(stmt_property, params)



# property_address
stmt_property_address = text("""
    INSERT INTO property_address (
        property_id, street_name, city, state, zipcode
    ) VALUES (
        :property_id, :street_name, :city, :state, :zipcode
    )
    ON CONFLICT (property_id) DO NOTHING;
""")

for _, row in data.iterrows():
    if pd.notnull(row["property_id"]) and pd.notnull(row["street_name"]):
        params = {
            "property_id": int(row["property_id"]),
            "street_name": row["street_name"] if not pd.isnull(row["street_name"]) else None,
            "city": row["city"] if not pd.isnull(row["city"]) else None,
            "state": row["state"] if not pd.isnull(row["state"]) else None,
            "zipcode": row["zipcode"] if not pd.isnull(row["zipcode"]) else None
        }
        connection.execute(stmt_property_address, params)



# agency
stmt_agency = text("""
    INSERT INTO agency (
        agency_id, agency_name, agency_number
    ) VALUES (
        :agency_id, :agency_name, :agency_number
    )
    ON CONFLICT (agency_id) DO NOTHING;
""")

for _, row in data.iterrows():
    if pd.notnull(row["agency_id"]) and pd.notnull(row["agency_name"]):
        params = {
            "agency_id": int(row["agency_id"]),
            "agency_name": row["agency_name"].strip() if not pd.isnull(row["agency_name"]) else None,
            "agency_number": row["agency_num"].strip() if "agency_num" in row and not pd.isnull(row["agency_num"]) else None
        }
        connection.execute(stmt_agency, params)



# agency_address
stmt_agency_address = text("""
    INSERT INTO agency_address (
        agency_id, street_name_1, street_name_2, city, state, zipcode
    ) VALUES (
        :agency_id, :street_name_1, :street_name_2, :city, :state, :zipcode
    )
    ON CONFLICT (agency_id) DO NOTHING;
""")

for _, row in data.iterrows():
    params = {
        "agency_id": row["agency_id"],
        "street_name_1": row["street_name_1"],
        "street_name_2": row["street_name_2"],
        "city": row["city"],
        "state": row["state"],
        "zipcode": row["zipcode"]
    }
    connection.execute(stmt_agency_address, params)



# agent
stmt_agent = text("""
    INSERT INTO agent (
        agent_id, agent_firstname, agent_lastname, agency_id
    ) VALUES (
        :agent_id, :agent_firstname, :agent_lastname, :agency_id
    )
    ON CONFLICT (agent_id) DO NOTHING;  -- Avoids duplicate entries
""")

for _, row in data.iterrows():
    params = {
        "agent_id": row["agent_id"],
        "agent_firstname": row["First_Name"],
        "agent_lastname": row["Last_Name"],
        "agency_id": row["agency_id"]
    }
    connection.execute(stmt_agent, params)



# agent_property
stmt_agent_property = text("""
    INSERT INTO agent_property (
        agent_id, property_id
    ) VALUES (
        :agent_id, :property_id
    )
    ON CONFLICT DO NOTHING;  -- Avoids duplicate entries
""")

for _, row in data.iterrows():
    params = {
        "agent_id": row["agent_id"],
        "property_id": row["property_id"]
    }
    connection.execute(stmt_agent_property, params)


# close the connection
connection.close()



"""
FOR TESTING:
stmt_view = "SELECT * FROM property_address;"
df = pd.read_sql(stmt_view, connection)
print(df)
"""