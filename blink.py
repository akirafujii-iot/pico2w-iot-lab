from machine import Pin, mem32
import time

PIR_PIN = 16
pir = Pin(PIR_PIN, Pin.IN, Pin.PULL_DOWN)
red = Pin(15, Pin.OUT)

# RP2350-E9対策：入力回路を「読む瞬間だけ」ONにする
PAD = 0x40038000 + 0x04 + PIR_PIN * 4  # GP16の設定レジスタの場所
IE = 1 << 6                             # 入力回路をONにするビット
SET, CLR = 0x2000, 0x3000               # ビットをON／OFFする専用の場所

def read_pir():
    mem32[PAD + SET] = IE   # 入力回路をON
    v = pir.value()
    mem32[PAD + CLR] = IE   # すぐOFFに戻す
    return v

mem32[PAD + CLR] = IE  # 普段は入力回路をOFFにしておく

print("センサー安定待ち30秒…")
time.sleep(30)
print("テスト開始")

last = None
start = time.ticks_ms()
while True:
    v = read_pir()
    if v != last:
        t = time.ticks_diff(time.ticks_ms(), start) // 1000
        print(t, "秒:", "検知" if v else "なし")
        red.value(v)
        last = v
    time.sleep(0.1)