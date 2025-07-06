mode = int(input("[0] 离线模式\n[1] 在线模式\n"))
if mode == 1:
    print("----online----")
    from online_main import start_online
    start_online()
else:
    print("----offline----")
    from offline_main import start_offline
    start_offline()
