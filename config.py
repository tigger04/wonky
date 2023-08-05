panels = [
    {
        "name": "tugenda",
        "top": 0.05,
        "left": 0.03,
        # "margin": 10,
        "maxheight": 0.4,
        "maxwidth": 0.2,
        "name": "agenda",
        "command": ["./tugenda", "today", "other" ],
        "outputType": "plaintext",
        "period": 60,
        "fontsize": 16,
        "textColor": [255, 255, 255, 190],
        "bgColor": [0, 0, 0, 50],
        "autoresize": True,
    },
    {
        "name": "priorities",
        "top": 0.2,
        "maxwidth": 0.5,
        "minwidth": 0.001,
        "command": ['~/wonky/priorities', '3'],
        "outputType": "plaintext",
        "linewrap": False,
        "period": 60,
        "align": "topcenter",
        "textAlign": "left",
        "fontsize": 0.018,
        "textColor": [255, 255, 255, 255],
        "bgColor": [0, 0, 0, 50],
        "autoresize": True,
    },
    {
        "name": "backup-status",
        "bottom": 0.18,
        "maxwidth": 0.5,
        "command": ["bash", "-c", "cat ~/wonky/backup.status | tr -d '\n'"],
        "outputType": "plaintext",
        "period": 60,
        "align": "bottomcenter",
        "textAlign": "center",
        "fontsize": 0.017,
        # "fontsize": 0.014,
        "textColor": [100, 100, 255, 255],
        "bgColor": [0, 0, 0, 0],
        "autoresize": True,
    },
    # {
    #     "name": "stats",
    #     "top": 0.03,
    #     "right": 0,
    #     "command": ["./system-stats"],
    #     "period": 4,
    #     "align": "topright",
    #     "outputType": "plaintext",
    #     "textColor": [255, 255, 255, 255],
    #     "font": "Apple Color Emoji",
    #     # "fontsize": 0.01,
    #     "textAlign": "right",
    #     "autoresize": True,
    # },
    {
        "name": "weather",
        "align": "bottomcenter",
        "outputType": "plaintext",
        "command": ["./weather", "--wonkydetail"],
        "period": 60,
        "bottom": 0.02,
        "font": "White Rabbit",
        "textAlign": "center",
        "textColor": [200, 200, 200, 255],
        "autoresize": True,
    },
    {
        "name": "calendar",
        "align": "bottomleft",
        "left": 0.03,
        "bottom": 0.05,
        "maxwidth": 0.20,
        "outputType": "html",
        "command": ["./calendar.lua"],
        "period": 300,
        "autoresize": True,
        "fontsize": 16,
    },
    {
        "name": "time",
        "bottom": 0.01,
        "align": "bottomcenter",
        "name": "time",
        "command": [
            "./showtime",
            "-t",
        ],
        "period": 60,
        "font": "Bohemian Typewriter",
        "fontsize": 0.18,
        "textAlign": "center",
        "textColor": [180, 180, 180, 120],
        "autoresize": True,
        "outputType": "plaintext",
    },
    {
        "name": "date",
        "top": 0.02,
        "align": "topcenter",
        "name": "date",
        "command": ["/bin/date", "+%A %-d"],
        "period": 60,
        "font": "Bohemian Typewriter",
        "fontsize": 0.1,
        "textAlign": "center",
        "textColor": [180, 180, 180, 120],
        "autoresize": True,
        "outputType": "plaintext",
    },
    {
        "name": "month",
        "top": 0.125,
        "align": "topcenter",
        "command": ["/bin/date", "+%B %Y"],
        "period": 60,
        "font": "Bohemian Typewriter",
        "fontsize": 0.02,
        "textAlign": "center",
        "textColor": [180, 180, 180, 120],
        "outputType": "plaintext",
    },
    {
        "name": "git-status",
        "align": "topright",
        "top": 0.13,
        "right": 0,
        # "left": 0.15,
        "maxwidth": 0.08,
        # "fontsize": 0.01,
        "period": 45,
        "outputType": "ansi",
        "command": ["./quick-git-status", "--env"],
        "autoresize": True,
    },
]
