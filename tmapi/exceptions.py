# Copyright 2011 Jamie Norrish (jamie@artefact.org.nz)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Module containing TMAPI exception classes."""

class IllegalArgumentException (Exception):

    """Exception to match Java's exception of the same name."""

    pass


class UnsupportedOperationException (Exception):

    """Exception to match Java's exception of the same name."""

    pass


class TMAPIException (Exception):

    """Base class for all standard (non run-time) exceptions thrown by
    a TMAPI system."""

    pass


class FactoryConfigurationException (TMAPIException):

    """Exception raised when a `TopicMapSystemFactory` instance cannot
    be instantiated through the method
    TopicMapSystemFactory.newInstance()."""
    pass


class FeatureNotRecognizedException (FactoryConfigurationException):

    """Exception raised when the TopicMapSystemFactory does not
    recognize the name of a feature that the application is trying to
    enable or disable."""

    pass


class FeatureNotSupportedException (FactoryConfigurationException):

    """Exception raised when the underlying implementation cannot
    support enabling or disabling a recognised feature. If the feature
    name is not recognised, implementations must throw a
    FeatureNotRecognizedException rather than a
    FeatureNotSupportedException."""

    pass


class TMAPIRuntimeException (Exception):

    """Base class for TMAPI runtime exceptions.

    Instances of this exception class should be thrown in cases where
    there is an error in the underlying topic map processing system or
    when integrity constraints are violated.

    """

    def __init__ (self, message=None, cause=None):
        """Constructs a new exception with the specified detail
        message.

        :param message: the optional detail message
        :type message: string
        :param cause: the optional exception that caused this
          exception to be raised
        :type cause: `Exception`

        """
        self._message = message
        self._cause = cause

    def __str__ (self):
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
