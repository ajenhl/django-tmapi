class Index (object):

    """Base class for all indices."""

    def __init__ (self, topic_map):
        self.topic_map = topic_map
        self._open = False

    def close (self):
        """Close the index."""
        self._open = False

    def is_auto_updated (self):
        """Indicates whether the index is updated automatically.

        If the value is True, then the index is automatically kept
        synchronized with the topic map as values are changed. If the
        value is False, then the `reindex()` method must be called to
        resynchronize the index with the topic map after values are
        changed.

        :rtype: boolean

        """
        return True
        
    def is_open (self):
        """Indicates if the index is open.

        :rtype: boolean

        """
        return self._open

    def open (self):
        """Opens the index.

        This method must be invoked before using any other method
        (aside from `is_open()`) in this class or derived classes.

        """
        self._open = True

    def reindex (self):
        """Synchronizes the index with data in the topic map."""
        pass
            
