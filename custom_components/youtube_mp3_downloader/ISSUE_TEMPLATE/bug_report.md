name: Bug Report
description: Report a bug with the YouTube MP3 Downloader integration
title: "[BUG] "
labels: ["bug"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for reporting a bug! Please provide as much information as possible.
  - type: input
    id: version
    attributes:
      label: Integration Version
      description: What version of the integration are you running?
      placeholder: "1.0.0"
    validations:
      required: true
  - type: input
    id: ha_version
    attributes:
      label: Home Assistant Version
      description: What version of Home Assistant are you running?
      placeholder: "2024.1.0"
    validations:
      required: true
  - type: textarea
    id: description
    attributes:
      label: Description
      description: Describe the bug in detail
    validations:
      required: true
  - type: textarea
    id: steps
    attributes:
      label: Steps to Reproduce
      description: Steps to reproduce the behavior
      placeholder: |
        1. Go to...
        2. Click...
        3. See error...
    validations:
      required: true
  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: What did you expect to happen?
    validations:
      required: true
  - type: textarea
    id: logs
    attributes:
      label: Relevant Logs
      description: Paste any relevant logs from Home Assistant
      render: logs
  - type: textarea
    id: additional
    attributes:
      label: Additional Context
      description: Any other context about the problem
