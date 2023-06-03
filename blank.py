def update_lossy_count(self, newEvent):
    current_bucket = int(math.ceil(self.observed_events / self.bucket_width))

    if newEvent.get_event_name() in self.events:  # if event exist
        lastEvent = self.events[newEvent.get_event_name()]  # save former event locally
        del self.events[newEvent.get_event_name()]  # increment event frequency
        self.events[newEvent.get_event_name()] = (lastEvent[0] + 1, lastEvent[1])
    else:
        self.events[newEvent.get_event_name()] = (1, current_bucket - 1)  # add the event

    if self.observed_events % self.bucket_width == 0.0:  # cleanup time based on max aproximation error
        tobedel = []
        for event, (frequency, bucket) in self.events.items():  # finds all keys to be removed
            if (frequency + bucket <= current_bucket):
                tobedel.append(event)
        for eventName in tobedel:  # cant be deleted on previous for loop as it moves it around
            del self.events[eventName]




