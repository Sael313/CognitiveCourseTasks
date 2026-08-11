### events
| ستون | نوع |
|---|---|
| uuid | UUID |
| event | String |
| properties | String |
| timestamp | DateTime64(6, 'UTC') |
| team_id | Int64 |
| distinct_id | String |
| elements_chain | String |
| created_at | DateTime64(6, 'UTC') |
| person_id | UUID |
| person_created_at | DateTime64(3) |
| person_properties | String |
| group0_properties | String |
| group1_properties | String |
| group2_properties | String |
| group3_properties | String |
| group4_properties | String |
| group0_created_at | DateTime64(3) |
| group1_created_at | DateTime64(3) |
| group2_created_at | DateTime64(3) |
| group3_created_at | DateTime64(3) |
| group4_created_at | DateTime64(3) |
| person_mode | Enum8('full' = 0, 'propertyless' = 1, 'force_upgrade' = 2) |
| historical_migration | Bool |
| dmat_string_0 | Nullable(String) |
| dmat_string_1 | Nullable(String) |
| dmat_string_2 | Nullable(String) |
| dmat_string_3 | Nullable(String) |
| dmat_string_4 | Nullable(String) |
| dmat_string_5 | Nullable(String) |
| dmat_string_6 | Nullable(String) |
| dmat_string_7 | Nullable(String) |
| dmat_string_8 | Nullable(String) |
| dmat_string_9 | Nullable(String) |
| $group_0 | String |
| $group_1 | String |
| $group_2 | String |
| $group_3 | String |
| $group_4 | String |
| $window_id | String |
| $session_id | String |
| $session_id_uuid | Nullable(UInt128) |
| elements_chain_href | String |
| elements_chain_texts | Array(String) |
| elements_chain_ids | Array(String) |
| elements_chain_elements | Array(Enum8('a' = 1, 'button' = 2, 'form' = 3, 'input' = 4, 'select' = 5, 'textarea' = 6, 'label' = 7)) |
| properties_group_custom | Map(String, String) |
| properties_group_ai | Map(String, String) |
| properties_group_feature_flags | Map(String, String) |
| person_properties_map_custom | Map(String, String) |
| _timestamp | DateTime |
| _offset | UInt64 |
| inserted_at | Nullable(DateTime64(6, 'UTC')) |
| consumer_breadcrumbs | Array(String) |
| is_deleted | Bool |
| mat_$ai_trace_id | Nullable(String) |
| mat_$ai_session_id | Nullable(String) |
| mat_$ai_is_error | Nullable(String) |
| mat_$ai_prompt_name | Nullable(String) |
| mat_$ai_experiment_id | Nullable(String) |

### person
| ستون | نوع |
|---|---|
| id | UUID |
| created_at | DateTime64(3) |
| team_id | Int64 |
| properties | String |
| is_identified | Int8 |
| is_deleted | Int8 |
| version | UInt64 |
| last_seen_at | Nullable(DateTime64(3)) |
| _timestamp | DateTime |
| _offset | UInt64 |

### session_replay_events
| ستون | نوع |
|---|---|
| session_id | String |
| team_id | Int64 |
| distinct_id | String |
| min_first_timestamp | SimpleAggregateFunction(min, DateTime64(6, 'UTC')) |
| max_last_timestamp | SimpleAggregateFunction(max, DateTime64(6, 'UTC')) |
| block_first_timestamps | SimpleAggregateFunction(groupArrayArray, Array(DateTime64(6, 'UTC'))) |
| block_last_timestamps | SimpleAggregateFunction(groupArrayArray, Array(DateTime64(6, 'UTC'))) |
| block_urls | SimpleAggregateFunction(groupArrayArray, Array(String)) |
| first_url | AggregateFunction(argMin, Nullable(String), DateTime64(6, 'UTC')) |
| all_urls | SimpleAggregateFunction(groupUniqArrayArray, Array(String)) |
| click_count | SimpleAggregateFunction(sum, Int64) |
| keypress_count | SimpleAggregateFunction(sum, Int64) |
| mouse_activity_count | SimpleAggregateFunction(sum, Int64) |
| active_milliseconds | SimpleAggregateFunction(sum, Int64) |
| console_log_count | SimpleAggregateFunction(sum, Int64) |
| console_warn_count | SimpleAggregateFunction(sum, Int64) |
| console_error_count | SimpleAggregateFunction(sum, Int64) |
| size | SimpleAggregateFunction(sum, Int64) |
| message_count | SimpleAggregateFunction(sum, Int64) |
| event_count | SimpleAggregateFunction(sum, Int64) |
| snapshot_source | AggregateFunction(argMin, LowCardinality(Nullable(String)), DateTime64(6, 'UTC')) |
| snapshot_library | AggregateFunction(argMin, Nullable(String), DateTime64(6, 'UTC')) |
| _timestamp | SimpleAggregateFunction(max, DateTime) |
| is_deleted | SimpleAggregateFunction(max, UInt8) |
| ai_tags_fixed | SimpleAggregateFunction(groupUniqArrayArray, Array(String)) |
| ai_tags_freeform | SimpleAggregateFunction(groupUniqArrayArray, Array(String)) |
| ai_highlighted | SimpleAggregateFunction(max, UInt8) |
| surfacing_score | SimpleAggregateFunction(max, Nullable(Float32)) |
| retention_period_days | SimpleAggregateFunction(max, Nullable(Int64)) |

