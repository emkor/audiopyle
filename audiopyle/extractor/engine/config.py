from commons.utils.env_var import read_env_var

broker_url = 'pyamqp://rabbitmq:rabbitmq@{}//'.format(read_env_var("RABBITMQ_SERIVCE_HOST", str))
result_backend = 'db+mysql://audiopyle:audiopyle@{}:{}/audiopyle'.format(read_env_var("MYSQL_SERVICE_HOST", str),
                                                                         read_env_var("MYSQL_SERVICE_PORT", int))

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Europe/Warsaw'
enable_utc = True

worker_concurrency = read_env_var("EXTRACTION_CONCURRENCY", int,
                                  default=2)  # concurrent tasks at a time per worker
task_acks_late = True

broker_pool_limit = read_env_var("EXTRACTION_BROKER_CONN_POOL_SIZE", int, default=4)

worker_prefetch_multiplier = 1
worker_max_tasks_per_child = 1
worker_max_memory_per_child = read_env_var("EXTRACTION_MEMORY_LIMIT_MB", int, default=256) * 1000
worker_send_task_events = True
task_send_sent_event = True
task_track_started = True
task_soft_time_limit = read_env_var("EXTRACTION_SOFT_TIME_LIMIT_SECONDS", float,
                                    default=2 * 60)  # exception within task is raised after: 2 minutes
task_time_limit = read_env_var("EXTRACTION_HARD_TIME_LIMIT_SECONDS", float,
                               default=5 * 60)  # worker process is killed after: 5 minutes
