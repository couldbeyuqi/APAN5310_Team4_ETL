CREATE TABLE property (
    property_id INTEGER PRIMARY KEY,
    price NUMERIC(12, 2),
    bedroom_number INTEGER,
    bathroom_number INTEGER,
    price_per_unit NUMERIC(12, 2),
    living_space NUMERIC(10, 2),
    land_space NUMERIC(10, 2),
    land_space_unit VARCHAR(50),
    property_type VARCHAR(50) NOT NULL,
    property_status VARCHAR(50)
);

CREATE TABLE property_address (
    property_id INTEGER PRIMARY KEY,
    street_name VARCHAR(255),
    city VARCHAR(100),
    state CHAR(2),
    zipcode VARCHAR(10),
    CONSTRAINT fk_property_address FOREIGN KEY (property_id) REFERENCES property (property_id)
);

CREATE TABLE agency (
    agency_id INTEGER PRIMARY KEY,
    agency_name VARCHAR(255) NOT NULL,
    agency_number VARCHAR(25)
);

CREATE TABLE agency_address (
    agency_id INTEGER PRIMARY KEY,
    street_name_1 VARCHAR(255),
    street_name_2 VARCHAR(255),
    city VARCHAR(100),
    state CHAR(2),
    zipcode VARCHAR(10),
    CONSTRAINT fk_agency_address FOREIGN KEY (agency_id) REFERENCES agency (agency_id)
);

CREATE TABLE agent (
    agent_id INTEGER PRIMARY KEY,
    agent_firstname VARCHAR(255),
    agent_lastname VARCHAR(255),
    agency_id INTEGER,
    CONSTRAINT fk_agent_agency FOREIGN KEY (agency_id) REFERENCES agency (agency_id)
);

CREATE TABLE agent_property (
    agent_id INTEGER,
    property_id INTEGER,
    PRIMARY KEY (agent_id, property_id),
    CONSTRAINT fk_agent_property_agent FOREIGN KEY (agent_id) REFERENCES agent (agent_id),
    CONSTRAINT fk_agent_property_property FOREIGN KEY (property_id) REFERENCES property (property_id)
);
