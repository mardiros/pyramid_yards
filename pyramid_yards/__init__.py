"""
pyramid_yards is a helpers for validating for on Pyramid

See the README.rst file for more information.
"""

__version__ = '0.16'
import logging

from pyramid.events import NewRequest
from pyramid.settings import asbool
from pyramid.exceptions import ConfigurationError

from .yards import Yards, RequestSchemaPredicate, ValidationFailure


def subscribe_yards(event):
    request = event.request
    request.set_property(Yards(request), 'yards', reify=True)


def includeme(config):
    settings = config.registry.settings
    try:
        config.add_translation_dirs('colander:locale')
    except ConfigurationError:
        log = logging.getLogger(__name__)
        log.error('Colander locales not found (Fix the colander package)')
    RequestSchemaPredicate.check_csrf_token = asbool(
        settings.get('pyramid_yards.check_csrf_token', 'true'))
    config.add_subscriber(subscribe_yards, NewRequest)
    config.add_view_predicate('request_schema', RequestSchemaPredicate)

    config.add_translation_dirs('pyramid_yards:locales'
                                )
