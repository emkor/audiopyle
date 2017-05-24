broker_url = 'pyamqp://rabbitmq:rabbitmq@rabbit1//'
result_backend = 'redis://redis1'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Europe/Warsaw'
enable_utc = True

worker_concurrency = 2  # maximum worker-processes -> 2 tasks at a time per worker
task_acks_late = True

broker_pool_limit = 4

worker_prefetch_multiplier = 1
worker_max_tasks_per_child = 1
worker_max_memory_per_child = 128 * 1000  # 128 MB
worker_send_task_events = True
task_send_sent_event = True
task_track_started = True
task_soft_time_limit = 2 * 60  # exception within task is raised after: 2 minutes
task_time_limit = 5 * 60  # worker process is killed after: 5 minutes
