"""Module containing TMAPI exception classes."""

class TMAPIException (Exception):

    """Base class for all standard (non run-time) exceptions thrown by
    a TMAPI system."""

    pass


class TMAPIRuntimeException (Exception):

    """Base class for TMAPI runtime exceptions.

    Instances of this exception class should be thrown in cases where
    there is an error in the underlying topic map processing system or
    when integrity constraints are violated.

    """

    def __init__ (self, message=None):
        self._message = message

    def __unicode__ (self):
        return self._message
    

class ModelConstraintException (TMAPIRuntimeException):

    """This exception is used to report Topic Maps - Data Model
    constraint violations."""

    def __init__ (self, reporter, message):
        """Creates a new ModelConstraintException with the specified
        message.

        :param reporter: the construct which has thrown this exception
        :type reporter: `Construct`
        :param message: the detail message
        :type message: string

        """
        self._reporter = reporter
        self._message = message
    
    def get_reporter (self):
        """Return the `Construct` which has thrown the exception.

        :rtype: `Construct`

        """
        return self._reporter


class IdentityConstraintException (ModelConstraintException):

    """This exception is used to report identity constraint
    violations. Assigning an item identifier, a subject identifier, or
    a subject locator to different objects causes an
    `IdentityConstraintException` to be raised."""

    def __init__ (self, reporter, existing, locator, message):
        """Creates a new `IdentityConstraintException` with the
        specified message.

        :param reporter: the construct to which the identity should
          have been assigned
        :type reporter: `Construct`
        :param existing: the construct that has the same identity
        :type existing: `Construct`
        :param locator: the locator representing the identity
        :type locator: `Locator`
        :param message: the detail message
        :type message: string

        """
        super(IdentityConstraintException, self).__init__(reporter, message)
        self._existing = existing
        self._locator = locator

    def get_existing (self):
        """Returns the `Construct` which already has the identity
        represented by the locator get_locator().

        :rtype: `Construct`

        """
        return self._existing

    def get_locator (self):
        """Returns the `Locator` representing the identity that caused
        the exception.

        :rtype: `Locator`

        """
        return self._locator


class MalformedIRIException (TMAPIRuntimeException):

    """Thrown to indicate that a malformed IRI has occurred."""

    def __init__ (self, message):
        """Constructs a `MalformedIRIException` with the specified
        detail message."""
        super(MalformedIRIException, self).__init__(message)


class TopicInUseException (ModelConstraintException):

    """Thrown when an attempt is made to remove a `Topic` which is
    being used as a type, as a reifier, or as a role player in an
    association, or in a scope."""
    
    def __init__ (self, topic, message):
        """Creates a new `TopicInUseException` with the specified message.

        :param topic: the topic which is not removable
        :type topic: `Topic`
        :param message: the detail message
        :type message: string

        """
        super(TopicInUseException, self).__init__(topic, message)


class TopicMapExistsException (TMAPIException):

    """Exception thrown when an attempt is made to create a new
    `TopicMap` under a storage address (an IRI) that is already
    assigned to another `TopicMap` in the same `TopicMapSystem`."""

    pass
