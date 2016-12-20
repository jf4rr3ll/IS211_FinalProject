DROP TABLE IF EXISTS posts;

CREATE TABLE posts(
PostID INTEGER PRIMARY KEY,
Author VARCHAR NOT NULL,
Title VARCHAR NOT NULL,
Content VARCHAR NOT NULL
Date DATE NOT NULL);

INSERT INTO posts VALUES
(1, admin, "Cryogenic Array", "Cryogenic Array: Offline. Premature termination resulting in system failure. Isolated manual and remote overrides detected. Controls disabled.", "12/1/2016"),
(2, admin, "Life Support", "Life Support: Offline. Premature termination resulting in system failure. Isolated manual and remote overrides detected. Controls disabled.", "12/5/2016"),
(3, admin, "VAULT 111 SECURITY INSTRUCTIONS", "CONFIDENTIAL CONFIDENTIAL CONFIDENTIAL, SECURITY EYES ONLY | VIOLATION VTP-01011. Vault 111 is designed to test the long-term effects of suspended animation on unaware, human subjects. Security staff are responsible for maintaining installation integrity and monitoring science staff activity. Under no circumstances are staff allowed to deviate from assigned duties. Insubordination or interference with vault operations are capital offenses. Security staff are authorized to use lethal force.", "12/7/16");