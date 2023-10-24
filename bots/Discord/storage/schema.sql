CREATE TABLE IF NOT EXISTS `geospatial_jobs` (
  `user_id` varchar(20) NOT NULL,
  `job_id` varchar(20),
  `result_id` varchar(20),
  `created_at` timestamp  DEFAULT CURRENT_TIMESTAMP
);