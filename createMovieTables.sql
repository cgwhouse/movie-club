CREATE TABLE Movies
(
  movie_ID INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  picker_ID INTEGER,
  watched INTEGER,
  UNIQUE(title),
  FOREIGN KEY (picker_ID) REFERENCES Members(member_ID)
);

CREATE TABLE Members
(
  member_ID INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  UNIQUE(name)
);

CREATE TABLE ProgramInfo
(
  current_selector INTEGER
);
