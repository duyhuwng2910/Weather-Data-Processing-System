-- macros/date_vars.sql

{% macro today() %}
  {{ modules.datetime.date.today() }}
{% endmacro %}

{% macro yesterday() %}
  {{ (modules.datetime.date.today() - modules.datetime.timedelta(days=1)) }}
{% endmacro %}

{% macro n_days_ago(n) %}
  {{ (modules.datetime.date.today() - modules.datetime.timedelta(days=n)) }}
{% endmacro %}

{% macro present_hour()%}
  {{ modules.datetime.datetime.now().replace(minute=0, second=0, microsecond=0).strftime('%d-%m-%Y %H:00:00') }}
{% endmacro %}

{% macro one_hour_ago() %}
  {{ (modules.datetime.datetime.now() - modules.datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S') }}
{% endmacro %}

{% macro start_of_month() %}
  {{ modules.datetime.date.today().replace(day=1) }}
{% endmacro %}
