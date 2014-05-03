class EventDispatcher:

    def trigger(self, event, *args, **kwargs):
        """
        Trigger an event.
        """
        if not hasattr(self, 'events'):
            self.events = {}

        ev = self.events.get(event, set())

        for listener in ev:
            listener(self, *args, **kwargs)

        # notify the top of the state stack automatically
        if hasattr(self, 'state') and self.state:
            callback = getattr(self.state[-1], 'on_' + event, None)
            if callback:
                callback(*args, **kwargs)



    def register(self, event, listener):
        """
        Register an event listener.
        """

        if not hasattr(self, 'events'):
            self.events = {}

        ev = self.events.get(event)
        if ev:
            ev.add(listener)
        else:
            self.events[event] = { listener }

    def unregister(self, event, listener):
        """
        Remove an event listener.
        """

        if not hasattr(self, 'events'):
            self.events = {}

        ev = self.events.get(event)
        if ev:
            ev.remove(listener)
