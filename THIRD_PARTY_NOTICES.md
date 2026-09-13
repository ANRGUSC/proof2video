# Third-party notices

The production helpers were generalized from the mathematical-video workflow
created for Scott Moeller and Bhaskar Krishnamachari. The original helpers carried a BSD-3-Clause notice naming
Scott Moeller and Bhaskar Krishnamachari. That notice is retained below for
the derived typography helper; the standalone plugin is authored by Bhaskar
Krishnamachari. No paper, paper-specific derivation, speech recording, or
model weight from that project is part of this repository.

Dependencies are installed separately and retain their own licenses:

- Manim Community: MIT; https://github.com/ManimCommunity/manim
- kokoro-onnx: MIT; https://github.com/thewh1teagle/kokoro-onnx
- Kokoro model: upstream identifies Apache-2.0; weights and voices are not bundled.
- NumPy, Pillow, SoundFile, ONNX Runtime, FFmpeg, Poppler, and TeX distributions:
  consult the licenses supplied by the versions installed in your environment.

The [Lamport Proof project](https://github.com/WWresearch/lamport-proof), by
Wojciech Aleksander Wołoszyn (WWresearch), inspired the public distribution and
explicit proof-review workflow. Its code is not copied, and it is not a required
dependency. This plugin is independent of that project and of OpenAI, Manim, and
the Kokoro maintainers.

## Derived typography helper

Applies to `skills/proof-to-video/scripts/proof_video/typography.py`
within the plugin directory and its repository copy.

BSD 3-Clause License

Copyright (c) 2026, Scott Moeller and Bhaskar Krishnamachari
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
