# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""Flask 3.x compatibility shim for Flask extensions pinned to Flask 2.x APIs.

Flask 3 removed several internal symbols that older Flask extensions rely on:

* ``flask._app_ctx_stack`` — used by Flask-SQLAlchemy 2.5.x for session scoping
* ``flask.helpers.locked_cached_property`` — used by Flask-Babel 3.1.x

This module restores lightweight stand-ins so those extensions continue to
work unchanged, avoiding the breaking session-management changes introduced
in Flask-SQLAlchemy 3.0.

Import this module before any ``flask_sqlalchemy`` or ``flask_babel`` import.
"""
from __future__ import annotations

import threading

import flask
import flask.helpers

# --- flask._app_ctx_stack (removed in Flask 3) ---
if not hasattr(flask, "_app_ctx_stack"):
    from flask.globals import _cv_app

    class _CompatAppCtxStack:
        """Minimal stand-in for the removed ``flask._app_ctx_stack``."""

        @property
        def __ident_func__(self) -> object:
            return threading.get_ident

        @property
        def top(self) -> object:
            return _cv_app.get(None)

    flask._app_ctx_stack = _CompatAppCtxStack()  # noqa: E501

# --- flask.helpers.locked_cached_property (removed in Flask 3) ---
if not hasattr(flask.helpers, "locked_cached_property"):
    from werkzeug.utils import cached_property

    flask.helpers.locked_cached_property = cached_property  # noqa: E501
