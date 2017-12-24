from midiutil import MIDIFile
import pandas_datareader as web
import datetime

filename = "test_music/twitter_prices.mid"

start = datetime.datetime(2016,3,10)
end = datetime.date.today()

twitter_abbreviation = "TWTR" #Twitter

desired_high = 120
desired_low = 10

twitter_stock = web.DataReader(twitter_abbreviation, "yahoo", start, end)
prices = twitter_stock.get("Open")

low = min(prices)
high = max(prices)
print(low)
print(high)
print(prices)


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

with open(filename, "wb") as output_file:
    MyMIDI.writeFile(output_file)
