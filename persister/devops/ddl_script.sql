CREATE DATABASE audiopyle;

USE audiopyle;

CREATE TABLE plugin (
  id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
  plugin_key VARCHAR(100) NOT NULL,
  output VARCHAR(50) NOT NULL,
  CONSTRAINT plugin_unique UNIQUE (plugin_key, output)
);

CREATE TABLE track_source (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  type VARCHAR(50) NOT NULL,
  bucket_address VARCHAR(50) NOT NULL,
  bucket_name VARCHAR(50) NOT NULL,
  CONSTRAINT track_source_unique UNIQUE (type, bucket_address, bucket_name)
);

CREATE TABLE track (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  source_id INT UNSIGNED NOT NULL,
  filename VARCHAR(256) NOT NULL,
  bit_depth INT UNSIGNED NOT NULL,
  sample_rate INT UNSIGNED NOT NULL,
  frames_count BIGINT UNSIGNED NOT NULL,
  channels_count INT UNSIGNED NOT NULL,
  FOREIGN KEY (source_id) REFERENCES track_source(id),
  CONSTRAINT track_unique UNIQUE (source_id, filename)
);

CREATE TABLE segment (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  track_id BIGINT UNSIGNED NOT NULL,
  offset BIGINT UNSIGNED NOT NULL,
  length BIGINT UNSIGNED NOT NULL,
  FOREIGN KEY (track_id) REFERENCES track(id)
);

CREATE TABLE feature (
  id BIGINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
  plugin_id INT UNSIGNED NOT NULL,
  segment_id BIGINT UNSIGNED NOT NULL,
  FOREIGN KEY (plugin_id) REFERENCES plugin(id),
  FOREIGN KEY (segment_id) REFERENCES segment(id),
  CONSTRAINT feature_unique UNIQUE (plugin_id, segment_id)
);

CREATE TABLE raw_feature (
  id BIGINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
  feature_id BIGINT UNSIGNED NOT NULL,
  timestamp FLOAT NOT NULL,
  label VARCHAR(100),
  FOREIGN KEY (feature_id) REFERENCES feature(id)
);

CREATE TABLE raw_feature_value (
  id BIGINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
  raw_feature_id BIGINT UNSIGNED NOT NULL,
  position INT UNSIGNED NOT NULL,
  value FLOAT,
  FOREIGN KEY (raw_feature_id) REFERENCES raw_feature(id)
);
