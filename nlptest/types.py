from enum import Enum
from typing import Union, List

from pydantic import BaseModel


class BehaviorType(str, Enum):
    invariance = "invariance"
    directional = "directional"
    minimum_functionality = "minimum functionality"


class TaskType(str, Enum):
    sequence_classification = "sequence_classification"
    target_sequence_classification = "targeted_sequence_classification"
    span_classification = "span_classification"


class Span(BaseModel):
    start: int
    end: int
    label: Union[str, int]
    prob: float = None

    def __str__(self):
        return str(self.start) + "_" + str(self.end) + "_" + str(self.label)

    def __hash__(self):
        return hash(str(self))

    def __lt__(self, other):
        return str(self) < str(other)

    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return str(self.start) + "_" + str(self.end) + "_" + str(self.label) == \
                   str(other.start) + "_" + str(other.end) + "_" + str(other.label)


class SpanClassificationOutput(BaseModel):
    text: str
    y_pred: List[Span]
    y: List[Span]

    @property
    def success(self):
        if len(self.y) != len(self.y_pred):
            return False

        return sorted(self.y) == sorted(self.y_pred)


class SequenceClassificationOutput(BaseModel):
    text: str
    y_pred: Union[str, int]
    y_pred_prob: float = None
    y: Union[str, int]

    @property
    def success(self):
        return self.y == self.y_pred


class TargetedSequenceClassificationOutput(SequenceClassificationOutput):
    target: str


BehaviorOutput = Union[SpanClassificationOutput, SequenceClassificationOutput, TargetedSequenceClassificationOutput]
