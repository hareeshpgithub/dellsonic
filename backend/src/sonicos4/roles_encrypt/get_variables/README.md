---

- name: Gather facts
  setup:

- name: Get system Unix Time
  set_fact:
  # current_date: "{{ ansible_date_time.date }}"
  # current_time: "{{ ansible_date_time.time }}"
  unix_time: "{{ ansible_date_time.epoch }}"
  backup_before_config: "{{{{inventory_hostname}} ({{unix_time}}1B).txt}}"
  backup_after_config: "{{{{inventory_hostname}} ({{unix_time}}2A).txt}}"

# - name: Convert date

# set_fact:

# full_date: "{{ current_date.split('-')[2] }} {{ months[current_date.split('-')[1] | int] }} {{ current_date.split('-')[0] }}"

# vars:

# months:

# 1: "January"

# 2: "February"

# 3: "March"

# 4: "April"

# 5: "May"

# 6: "June"

# 7: "July"

# 8: "August"

# 9: "September"

# 10: "October"

# 11: "November"

# 12: "December"
