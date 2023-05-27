import numpy as np

def sample_array(arr, rate):
  arr = np.array(arr)
  if rate < 1:
    rate = int(1 / rate)
    num_samples = rate - 1
    print(num_samples)
    sampled = np.hstack([np.linspace(arr[i], arr[i+1], num_samples+2, endpoint=False)[1:] for i in range(len(arr)-1)])
    sampled = np.hstack([arr, sampled])
    sampled.sort()
  else:
    sampled = arr[::rate]
  return sampled

fps = 24

# times are in sec
def beats_deforum(beats, adsr_times, adsr_mags, every_n=1):
  decay, release = adsr_times
  on_value, decay_value, off_value = adsr_mags
  frames = [(0, off_value)]
  beats = sample_array(beats, every_n)
  for i in range(0, len(beats)):
    time = round(beats[i], 3)
    keyframes = np.transpose((np.round([time, time + decay, time + decay + release], 3), [on_value, decay_value, off_value]))
    frames.extend([(int(k[0] * fps), k[1]) for k in keyframes])
  frames = sorted(frames, key=lambda x: x[0])
  frames = [f"{frame}:({mag})" for frame, mag in frames]
  return ",".join(frames)

def beats_prompts(beat_times, prompts):
  prompt_idx = 0
  res = {
      0: prompts[0]
  }
  for i in range(len(beat_times)):
    time = round(beat_times[i], 3)
    frame = int(time * fps)
    prompt_idx = 0 if prompt_idx == len(prompts) - 1 else prompt_idx + 1
    res[frame] = prompts[prompt_idx]
  return res

