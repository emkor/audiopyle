from commons.utils.env_var import get_environment_variable

broker_url = 'pyamqp://rabbitmq:rabbitmq@rabbitmq_host//'
result_backend = 'db+mysql://celery:celery@mysql_host:3306/results'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Europe/Warsaw'
enable_utc = True

worker_concurrency = get_environment_variable("EXTRACTION_CONCURRENCY",
                                              default=2)  # concurrent tasks at a time per worker
task_acks_late = True

broker_pool_limit = get_environment_variable("EXTRACTION_BROKER_CONN_POOL_SIZE", default=4)

worker_prefetch_multiplier = 1
worker_max_tasks_per_child = 1
worker_max_memory_per_child = 128 * 1000  # 128 MB
worker_send_task_events = True
task_send_sent_event = True
task_track_started = True
task_soft_time_limit = get_environment_variable("EXTRACTION_SOFT_TIME_LIMIT_SECONDS",
                                                default=2 * 60)  # exception within task is raised after: 2 minutes
task_time_limit = get_environment_variable("EXTRACTION_HARD_TIME_LIMIT_SECONDS",
                                           default=5 * 60)  # worker process is killed after: 5 minutes
