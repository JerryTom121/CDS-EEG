import win32api

VK_MEDIA_PLAY_PAUSE = 0xB3
hwcode_pause_play = win32api.MapVirtualKey(VK_MEDIA_PLAY_PAUSE, 0)
VK_MEDIA_NEXT_TRACK = 0xB0
hwcode_next = win32api.MapVirtualKey(VK_MEDIA_NEXT_TRACK, 0)

def pause_play():
  win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, hwcode_pause_play)

def next_track():
  win32api.keybd_event(VK_MEDIA_NEXT_TRACK, hwcode_next)