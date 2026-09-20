"""Replace the upstream WLOC shortcut's parser endpoint with this deployment.

The output is an unsigned Shortcut source file for inspection and signing on
Apple devices. Run: python scripts/personalize-shortcut.py input.shortcut output.shortcut
"""

import plistlib
import sys
from pathlib import Path


OLD = "https://wloc.xepesw.workers.dev/api/parse?format=json&u="
NEW = "https://wloc.fengsx.workers.dev/api/parse?format=json&u="


def main(source: Path, destination: Path) -> None:
    with source.open("rb") as stream:
        shortcut = plistlib.load(stream)
    actions = shortcut["WFWorkflowActions"]
    matches = [
        action for action in actions
        if action["WFWorkflowActionIdentifier"] == "is.workflow.actions.downloadurl"
        and OLD in str(action["WFWorkflowActionParameters"].get("WFURL", ""))
    ]
    if len(matches) != 1:
        raise ValueError(f"Expected one parser request; found {len(matches)}")
    token = matches[0]["WFWorkflowActionParameters"]["WFURL"]["Value"]
    old_text = token["string"]
    if old_text != OLD + "\ufffc":
        raise ValueError("Unexpected parser URL layout")
    old_range = "{" + str(len(OLD)) + ", 1}"
    new_range = "{" + str(len(NEW)) + ", 1}"
    attachment = token["attachmentsByRange"].pop(old_range)
    token["string"] = NEW + "\ufffc"
    token["attachmentsByRange"][new_range] = attachment

    comment = actions[0]["WFWorkflowActionParameters"]
    if actions[0]["WFWorkflowActionIdentifier"] == "is.workflow.actions.comment":
        comment["WFCommentActionText"] = (
            "WLOC 自用版。解析服务: https://wloc.fengsx.workers.dev\n"
            "模块订阅: https://github.com/fengsx/wloc/tree/main/modules"
        )
    with destination.open("wb") as stream:
        plistlib.dump(shortcut, stream, fmt=plistlib.FMT_BINARY, sort_keys=False)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: personalize-shortcut.py input.shortcut output.shortcut")
    main(Path(sys.argv[1]), Path(sys.argv[2]))
