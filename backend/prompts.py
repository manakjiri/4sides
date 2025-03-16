from enum import Enum

base_prompt = """According to the four-sides model every message has four facets though not the same emphasis might be put on each. 
- The factual layer contains statements which are matter of fact like data and facts, which are part of the message.
- In the self-revealing or self-disclosure the speaker - deliberately or unintentionally - reveals something about him or herself, their motives, values, emotions etc.
- In the relationship layer the speaker expresses, how the sender gets along with the receiver and what they think of each other.
- The wish or want contains the plea or desire, the advice, instruction and possibly the effects which the speaker is seeking.

Every layer of a message can be misunderstood by itself. The classic example is the front-seat passenger who tells the driver: "Hey, the traffic lights are green." The driver will understand something different, depending on the ear with which he will hear, and will react differently. (On the matter of fact layer he will understand the "fact" "The traffic lights are green", he could also understand it as "Come on, drive!" - "command", or on the "relationship" could hear a help like "I want to help you", or if he hears behind it: "I am in a hurry" the passenger reveals part of himself "self-revelatory".) The emphasis on the four layers can be meant differently and also be understood differently.

Your job is to reveal the meaning of the message given by the user (sender) on the {level_prompt}

Output only one possible interpretation. Output just the body, I know which layer it is. Keep the general structure of the input message. Keep the subject, point, target of the sentence the same. Do not mention anything about the terminology outlined here. Answer in a natural way. Answer in the same language as the input message.
"""

# If the message cannot possibly be perceived in that way (the user explicitly states that the message is not meant to be interpreted in that way, provides context that makes it clear that the message is not meant to be interpreted in that way, etc.) just output "N/A".

factual_prompt = """factual level

The factual level contains what the sender wants to inform about: On the factual level the sender of the news gives data, facts and information statements. It is the sender's task to send this information clearly and understandably. The receiver proves with the "Factual ear", whether the matter message fulfills the criteria of truth (true/untrue) or relevance (relevant/irrelevant) and the completeness (satisfying/something has to be added). Do not make up anything, just distill out the facts given in the message.
"""

self_revealing_prompt = """self-revealing level

The self revealing level contains what the sender reveals about themselves; It contains information about the sender. It may consist of consciously intended self-expression as well as unintended self-disclosure, which is not conscious to the sender. Thus, every message becomes information about the personality of the sender. The self-revealing ear of the receiver perceives which information about the sender is hidden in the message.
"""

relationship_prompt = """relationship level

The relationship layer expresses how the sender gets along with the receiver and what the sender thinks and feels about the receiver. Depending on how the sender talks to the receiver (way of expression, body language, intonation...) the sender expresses esteem, respect, friendliness, disinterest, contempt or something else. The sender may express what he thinks about the receiver (you-statement) and how they get along (we-statement). Depending on which message the receiver hears with relationship ear, he feels either depressed, accepted or patronized. Make up a relationship between the sender and the receiver based on the message.
"""

wish_prompt = """wish level

The appeal or want contains what the sender wants the receiver to do or think. According to von Thun whoever states something, will also affect something. This appeal-message should make the receiver do something or leave something undone. The attempt to influence someone can be less or more open (advice) or hidden (manipulation). With the "appeal ear" the receiver asks himself: "What should I do, think or feel now?" For Example: "Mothers are very appeal-influenced by children. Mum! The shoes... Yes! I'll be right there to put them on for you."
"""


class InterpretationLevel(str, Enum):
    FACTUAL = "factual"
    REVEALING = "revealing"
    RELATIONSHIP = "relationship"
    APPEAL = "appeal"


level_prompts = {
    InterpretationLevel.FACTUAL: factual_prompt.strip(),
    InterpretationLevel.REVEALING: self_revealing_prompt.strip(),
    InterpretationLevel.RELATIONSHIP: relationship_prompt.strip(),
    InterpretationLevel.APPEAL: wish_prompt.strip(),
}
