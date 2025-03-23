import os
import time
import asyncio
import math

COLORS = {
    'header': '\033[94m',  # Blue
    'percentage': '\033[92m',  # Green
    'speed': '\033[93m',  # Yellow
    'eta': '\033[91m',  # Red
    'reset': '\033[0m'
}

class StreamProgress:
    def __init__(self):
        self.lock = asyncio.Lock()
        self.start_time = time.time()
        self.active = {}
        self.completed = 0
        self.last_update = 0

    async def update(self, file_id, current, total, filename):
        async with self.lock:
            now = time.time()

            if total <= 0:
                return

            # Initialize or update download entry
            if file_id not in self.active:
                self.active[file_id] = {
                    'filename': filename,
                    'total': total,
                    'start': now,
                    'last_bytes': current,
                    'last_time': now
                }
            else:
                # Update existing entry
                self.active[file_id]['current'] = current
                self.active[file_id]['total'] = total

            # Calculate speed and ETA
            entry = self.active[file_id]
            elapsed = now - entry['last_time']
            delta = current - entry['last_bytes']
            entry['speed'] = delta / elapsed if elapsed > 0 else 0
            entry['eta'] = self._calculate_eta(entry['total'] - current, entry['speed'])

            # Update tracking
            entry['last_bytes'] = current
            entry['last_time'] = now

            # Handle completion
            if current >= total:
                self.completed += 1
                del self.active[file_id]

            # Throttle updates to 10 FPS
            if now - self.last_update > 0.1:
                self._print_progress()
                self.last_update = now

    def _print_progress(self):
        terminal_width = os.get_terminal_size().columns
        line = []

        if self.active:
            # Get first active download (for single-line display)
            file_id, data = next(iter(self.active.items()))

            # Progress components
            progress = data['current'] / data['total']
            bar_width = max(20, terminal_width - 70)
            filled = int(bar_width * progress)

            # Formatting
            line.append(f"{COLORS['header']}⬇{COLORS['reset']} ")
            line.append(f"{self._truncate(data['filename'], 25)} ")
            line.append(f"{COLORS['percentage']}{progress*100:6.2f}%{COLORS['reset']} ")
            line.append(f"[{'='*filled}>{' '*(bar_width-filled)}] ")
            line.append(f"{COLORS['speed']}{self._format_size(data['current'])}/{self._format_size(data['total'])}{COLORS['reset']} ")
            line.append(f"{COLORS['speed']}{self._format_speed(data['speed'])}{COLORS['reset']} ")
            line.append(f"{COLORS['eta']}ETA: {data['eta']}{COLORS['reset']}")

            # Completed counter
            line.append(f" ({self.completed} done)")

            # Truncate to terminal width
            full_line = ''.join(line)
            print(f"\r{full_line[:terminal_width]}", end="", flush=True)
        else:
            elapsed = time.time() - self.start_time
            print(f"\r✅ Completed {self.completed} files in {elapsed:.1f}s".ljust(terminal_width), flush=True)

    def _calculate_eta(self, remaining, speed):
        if speed <= 0 or remaining <= 0:
            return "--:--"
        seconds = remaining / speed
        return f"{int(seconds//3600):02d}:{int((seconds%3600)//60):02d}:{int(seconds%60):02d}"

    def _format_speed(self, speed):
        if speed < 1024:
            return f"{speed:.1f} B/s"
        elif speed < 1024**2:
            return f"{speed/1024:.1f} KB/s"
        return f"{speed/(1024**2):.1f} MB/s"

    def _format_size(self, bytes):
        if bytes < 1024:
            return f"{bytes} B"
        elif bytes < 1024**2:
            return f"{bytes/1024:.1f} KB"
        elif bytes < 1024**3:
            return f"{bytes/(1024**2):.1f} MB"
        return f"{bytes/(1024**3):.1f} GB"

    def _truncate(self, text, max_len):
        return text[:max_len-2] + '..' if len(text) > max_len else text.ljust(max_len)
