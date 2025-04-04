--
-- drive_info.sql
--

-- Table for the drives 
CREATE TABLE IF NOT EXISTS drive(
    id INTEGER PRIMARY KEY AUTOINCREMENT,                                     -- id 
    name TEXT,                                                  -- name of the drive (encrypted)
    path BLOB,                                                  -- path to the drive (encrypted)
    current INTEGER NOT NULL CHECK (current IN (0, 1)),         -- status if current
    databpwd_id INTEGER,                                        -- id for the salt
    FOREIGN KEY (databpwd_id) REFERENCES databpwd(id)
);

-- Table for the encrypted password and salt
CREATE TABLE IF NOT EXISTS databpwd(
    id INTEGER PRIMARY KEY AUTOINCREMENT,                                     -- id
    password BLOB,                                              -- the encrypted password
    salt BLOB                                                   -- the salt of the password
);