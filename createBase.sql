CREATE TABLE IF NOT EXISTS ExamTypes (
    ID   INTEGER    PRIMARY KEY
                    UNIQUE
                    NOT NULL,
    Name TEXT (100) 
);

CREATE TABLE IF NOT EXISTS Faculties (
    ID   INTEGER    PRIMARY KEY
                    NOT NULL
                    UNIQUE,
    Name TEXT (100) UNIQUE
                    NOT NULL
);

CREATE TABLE IF NOT EXISTS FormEducations (
    ID   INTEGER    PRIMARY KEY
                    UNIQUE
                    NOT NULL,
    Name TEXT (100) NOT NULL
);

CREATE TABLE IF NOT EXISTS FundingSources (
    ID   INTEGER    PRIMARY KEY
                    NOT NULL
                    UNIQUE,
    Name TEXT (150) UNIQUE
                    NOT NULL
);

CREATE TABLE IF NOT EXISTS Specializations (
    ID   INTEGER    NOT NULL
                    UNIQUE
                    PRIMARY KEY,
    Name TEXT (100) UNIQUE
                    NOT NULL
);

CREATE TABLE IF NOT EXISTS SpecializationVariants (
    ID       INTEGER    PRIMARY KEY
                        NOT NULL
                        UNIQUE,
    Name     TEXT (100) NOT NULL,
    Cod      TEXT (20)  NOT NULL,
    Quantity INTEGER    NOT NULL
);

CREATE TABLE IF NOT EXISTS Abiturients (
    ID  INTEGER   PRIMARY KEY
                  NOT NULL
                  UNIQUE,
    Kod TEXT (20) UNIQUE
                  NOT NULL
);

CREATE TABLE IF NOT EXISTS Prioritets (
    ID            INTEGER    UNIQUE
                             NOT NULL
                             PRIMARY KEY,
    AbiturientID  INTEGER    REFERENCES Abiturients (ID) 
                             NOT NULL,
    FacultyID     INTEGER    REFERENCES Faculties (ID) 
                             NOT NULL,
    SpecID        INTEGER    REFERENCES Specializations (ID) 
                             NOT NULL,
    SpecVariantID INTEGER    REFERENCES SpecializationVariants (ID),
    Prioritet     INTEGER    NOT NULL,
    Status        TEXT (100) NOT NULL,
    NumSpis       INTEGER    NOT NULL,
    NumIfOrig     INTEGER    NOT NULL,
    FormEdID      INTEGER    REFERENCES FormEducations (ID) 
                             NOT NULL,
    FunSourceID   INTEGER    NOT NULL
                             REFERENCES FundingSources (ID) 
);

CREATE TABLE IF NOT EXISTS DynamicLists (
    ID              INTEGER    PRIMARY KEY
                               UNIQUE
                               NOT NULL,
    AbiturientID    INTEGER    NOT NULL
                               REFERENCES Abiturients (ID),
    PrioritetID     INTEGER    NOT NULL
                               REFERENCES Prioritets (ID),
    Mark1           TEXT (20)  NOT NULL,
    Mark2           TEXT (20)  NOT NULL,
    Mark3           TEXT (20)  NOT NULL,
    MarkID          TEXT (20)  NOT NULL,
    NumGeneral      INTEGER    NOT NULL,
    NumPrioritet    INTEGER    NOT NULL,
    TargetedID      TEXT (100),
    TargetedInfo    TEXT (200),
    OlympiadRank    TEXT (100),
    MainTopPriority TEXT (100),
    Privilege1      TEXT (100),
    Privilege2      TEXT (100),
    Privilege3      TEXT (100),
    ExamTypeID      INTEGER    REFERENCES ExamTypes (ID) 
);
