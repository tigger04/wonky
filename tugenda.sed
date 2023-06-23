s/^[[:space:]]+//g
s/^birthdays:[[:space:]]*/🎁 /g
s/^[a-zA-Z0-9\?\-]+:[[:space:]]*//g
s/^TODO/>/g
s/^IDEA/i/g
s/^APPT/📅/g
s/\[#[A-E]\] //g
s/^Today$/-->Today/g
s/^Other items/-->Other/g
s/^Scheduled: +(TODO )?/🟦 /g
s/^Sched\. *[0-9]+x: +(TODO|APPT )?/🟧 /g
s/^Deadline: +(TODO|APPT )?/⭕ /g
s/^[0-9]+[[:space:]]d\. ago: /🟥/g
s/[[:space:]]+/ /g
s/^In ([0-9]+) *d\.: *(TODO|APPT )?/📅+\1 /g
s/^HOLD /✋ /g
s/^ELAB /📖 /g
s/^([0-9]:[0-5][0-9][^0-9])/0\1/g
s/^([012][0-9]:[0-5][0-9])(-[012]?[0-9]:[0-5][0-9])?/\1/g
s/^([012][0-9]):00([^0-9])/\1h\2/g
s/^([012][0-9](:[0-5][0-9]|h))( Sched(uled|\.))?:?( APPT)?/🕐 \1/g
s/^([A-Za-z]+)/📅 \1/g
s/^(\([0-9]+\/[0-9]+\)): (.*)$/📅 \2/g
s/-->([a-zA-Z]+)/\U\1/g
