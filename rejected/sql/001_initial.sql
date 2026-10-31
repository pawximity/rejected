CREATE TABLE resume_types (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE applications (
  id INTEGER PRIMARY KEY,
  company TEXT NOT NULL,
  role TEXT NOT NULL,
  applied_at TEXT NOT NULL,
  resume_type_id INTEGER,
  source TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (resume_type_id) REFERENCES resume_types (id)
);


CREATE INDEX idx_applications_resume_type ON applications (resume_type_id);


CREATE TABLE application_events (
  id INTEGER PRIMARY KEY,
  application_id INTEGER NOT NULL,
  event_type TEXT NOT NULL,
  occurred_at TEXT NOT NULL,
  notes TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (application_id) REFERENCES applications (id)
);


CREATE INDEX idx_events_application ON application_events (application_id);