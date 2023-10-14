CREATE TABLE air_quality_sensors (
                id  INT NOT NULL AUTO_INCREMENT,
                entry_id INT NOT NULL,
                eCO2 FLOAT NOT NULL,
                eTVOC FLOAT NOT NULL,
                Temperature FLOAT NOT NULL,
                Air_pressure FLOAT NOT NULL,
                Humidity FLOAT NOT NULL,
                temperature_ FLOAT NOT NULL,
                Controller_temperature FLOAT NOT NULL,
                G FLOAT NOT NULL,          
                date_creation  VARCHAR(250) NOT NULL,       
                time_float FLOAT NOT NULL,                                      
                PRIMARY KEY (id)
);
