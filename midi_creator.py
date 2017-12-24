from midiutil import MIDIFile
import pandas_datareader as web
import datetime

filename = "test_music/twitter_prices.mid"

start = datetime.datetime(2016,3,10)
end = datetime.date.today()
# stock = "YAMHF" #Yamaha
stock = "TWTR" #Twitter

desired_high = 120
desired_low = 10

apple = web.DataReader(stock, "yahoo", start, end)
prices = apple.get("Open")

low = min(prices)
high = max(prices)
print(low)
print(high)
print(apple.get("Open"))


desired_range = desired_high - desired_low

shift = desired_low - low
weight = desired_range / (high - low)

new_prices = []
for i in range(len(prices)):
    new_prices.append(int(weight * (prices[i] - low) + 10))

print(new_prices)
count = 0
track    = 0
channel  = 0
time     = 0    # In beats
duration = 0.25    # In beats
tempo    = 360   # In BPM
volume   = 100  # 0-127, as per the MIDI standard

MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
                      # automatically)
MyMIDI.addTempo(track, time, tempo)

for i, pitch in enumerate(new_prices):
    MyMIDI.addNote(track, channel, int(pitch), time + i*duration, duration, volume)

# for i in range(12):
#     while time < 12:
#         MyMIDI.addNote(track, channel, pitch, time*.25 + i*3, duration, volume)
#         time += 1
#         pitch += 6
#     time = 0
#     pitch -= (6*12 - 1)

# count = 12
# num = 0
# track    = 0
# channel  = 0
# time     = 0    # In beats
# duration = 1./8    # In beats
# tempo    = 360   # In BPM
# volume   = 60  # 0-127, as per the MIDI standard
#
# MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
#                       # automatically)
# MyMIDI.addTempo(track, time, tempo)

# for i, pitch in enumerate(new_prices):
#     MyMIDI.addNote(track, channel, int(pitch), time + i*duration, duration, volume)

# for i in range(600):
#     MyMIDI.addNote(track, channel, random.randint(10, 110), time + i * duration, duration, volume)
# pitch = 110
# while count > 0:
#     for i in range(pitch,40,-4):
#         MyMIDI.addNote(track, channel, i, num * duration, duration, volume)
#         num += 1
#     pitch -= 10
#     count -= 1
# pitch = 110
# while count > 0:
#     for i in range(6):
#         print(((pitch - (12 * i)) + count))
#         MyMIDI.addNote(track, channel, ((pitch - (6 * i)) + count), num * duration, duration, volume)
#         num += 1
#     pitch -= 1
#     count -= 1
with open(filename, "wb") as output_file:
    MyMIDI.writeFile(output_file)
