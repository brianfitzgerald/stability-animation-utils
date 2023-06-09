from typing import List
import numpy as np

def sample_array(arr, rate):
    arr = np.array(arr)
    if rate < 1:
        rate = int(1 / rate)
        num_samples = rate - 1
        sampled = np.hstack(
            [
                np.linspace(arr[i], arr[i + 1], num_samples + 2, endpoint=False)[1:]
                for i in range(len(arr) - 1)
            ]
        )
        sampled = np.hstack([arr, sampled])
        sampled.sort()
    else:
        sampled = arr[::rate]
    return sampled

def as_beats(frames):
    frames = [f"{frame}:({mag})" for frame, mag in frames]
    return ",".join(frames)


class BeatVisuals:

    def __init__(self, beats, times, fps=24):
        self.fps = fps
        self.beats = times[beats]
        self.beats = np.insert(self.beats, 0, 0)
        self.max_frames = int(max(times) * fps)

    # times are in sec
    # adsr_times = decay, release
    # adsr_mags = on_value, decay_value, off_value
    def beats_deforum(
        self, decay: float, adsr_mags: List[float], every_n: int = 1
    ):
        on_value, off_value = adsr_mags
        frames = []
        beats = sample_array(self.beats, every_n)
        for i in range(0, len(beats)):
            time = round(beats[i], 3)
            keyframes = np.transpose(
                (
                    [time, time + decay],
                    [on_value, off_value],
                )
            )
            frames.extend([(int(k[0] * self.fps), k[1]) for k in keyframes])

        frames = sorted(frames, key=lambda x: x[0])

        # remove duplicate time entries
        found_keyframes = set()
        for kf, val in frames:
            if kf in found_keyframes:
                frames.remove((kf, val))
            else:
                found_keyframes.add(kf)
        return frames

    def as_xy(self, frames):
        frames = np.array(frames)
        x, y = frames[:, 0], frames[:, 1]
        x = x / self.fps
        return x, y

    def beats_prompts(self, prompts):
        prompt_idx = 0
        res = {0: prompts[0]}
        for i in range(len(self.beats)):
            time = round(self.beats[i], 3)
            frame = int(time * self.fps)
            prompt_idx = 0 if prompt_idx == len(prompts) - 1 else prompt_idx + 1
            res[frame] = prompts[prompt_idx]
        return res
