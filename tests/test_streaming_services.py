# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import time

from ansys.fluent.core import connect_to_fluent
from ansys.fluent.core.utils.fluent_version import FluentVersion


def transcript(data):
    transcript.data = data


def run_transcript(i, ip, port, password):
    transcript("")
    session = connect_to_fluent(
        ip=ip, port=port, password=password, cleanup_on_exit=False
    )
    session.transcript.register_callback(transcript)

    transcript_checked = False
    transcript_passed = False

    if i % 5 == 0:
        time.sleep(0.5)
        session.scheme_eval.scheme_eval("(pp 'test)")
        time.sleep(0.5)
        if not transcript.data:
            assert transcript.data == ""
        else:
            assert transcript.data == "test"
            transcript_passed = True
        transcript_checked = True

    return transcript_checked, transcript_passed


def test_transcript(new_solver_session):
    solver = new_solver_session
    ip = solver.connection_properties.ip
    port = solver.connection_properties.port
    password = solver.connection_properties.password

    total_checked_transcripts = 0
    total_passed_transcripts = 0

    for i in range(100):
        transcript_checked, transcript_passed = run_transcript(i, ip, port, password)
        total_checked_transcripts += int(transcript_checked)
        total_passed_transcripts += int(transcript_passed)

    if solver.get_fluent_version() >= FluentVersion.v232:
        assert total_checked_transcripts == total_passed_transcripts
    else:
        assert total_checked_transcripts >= total_passed_transcripts
