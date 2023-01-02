s/^[[:space:]]+//g
s/^[a-zA-Z0-9\-]+:[[:space:]]+//g
s/^TODO/>/g
s/^IDEA/i/g
s/\[#[A-E]\] //g
s/^Today$/-->Today/g
s/^Other items/-->Other/g
s/-->([a-zA-Z]+)/\U\1/g
s/^Scheduled: +(TODO)?/🕘/g
s/^Sched\. *[0-9]+x: +(TODO)?/🔴/g
s/^Deadline: +(TODO)?/🔵/g
s/^[0-9]+[[:space:]]d\. ago: /🟥/g
s/[[:space:]]+/ /g
s/^In ([0-9]+) *d\.: *TODO /📅+\1 /g
