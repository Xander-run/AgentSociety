from uuid import uuid4
import datetime

from agentsociety.survey import Survey
from agentsociety.survey.models import Page, Question, QuestionType
from agentsociety.configs.exp import (
    WorkflowStepConfig,
    WorkflowType,
)


def normal_run(days: int):
    return WorkflowStepConfig(
        type=WorkflowType.RUN,
        days=days,
        ticks_per_step=1800
    )

Survey1 = WorkflowStepConfig(
    type=WorkflowType.SURVEY,
    target_agent=[i for i in range(5, 105)],  # adjust this as needed
    survey=Survey(
        id=uuid4(),
        title="Perception and Coping Behaviors During Extreme Heat",
        description="""
            We are conducting research on public perception, health risk awareness, and coping strategies during extreme heat events. This survey aims to understand your experiences and behaviors during high-temperature periods. All responses are anonymous and will be used solely for statistical analysis. Please answer based on your actual experiences. This survey will take approximately 5-8 minutes to complete. Thank you for your participation!
                
            Response in JSON format.
            """,
        created_at=datetime.datetime.now(),
        pages=[
            Page(
                name="page1",
                elements=[
                    Question(
                        name="question1",
                        title="Unique ID",
                        type=QuestionType.TEXT,
                        required=True,
                    ),
                    Question(
                        name="question14",
                        title="Occupation Type",
                        type=QuestionType.CHECKBOX,
                        required=True,
                        choices=[
                            "Primarily indoor office work",
                            "Primarily outdoor/manual labor",
                            "Student",
                            "Retired/Unemployed",
                            "Freelancer/Remote worker"
                        ],
                    ),
                    Question(
                        name="question2",
                        title="How would you describe the recent high temperature period",
                        type=QuestionType.RADIO,
                        choices=[
                            "Extremely high, unbearable",
                            "Relatively high, felt hot",
                            "Moderate, acceptable",
                            "Not particularly high，same as usual",
                            "No feeling/unsure"
                        ]
                    ),
                    Question(
                        name="question5",
                        title="Do you believe extreme heat (e.g., heatwaves) negatively impacts health",
                        type=QuestionType.RADIO,
                        required=True,
                        choices=[
                            "Significant negative impact",
                            "Considerable negative impact",
                            "Some negative impact",
                            "Minimal negative impact",
                            "No negative impact"
                        ]
                    ),
                    Question(
                        name="question4",
                        title="Can adverse health effects from heat (e.g., heatstroke, cardiovascular strain) be effectively prevented?",
                        type=QuestionType.RADIO,
                        required=True,
                        choices=[
                            "Completely preventable",
                            "Mostly preventable",
                            "Partially preventable",
                            "Almost impossible to prevent",
                            "Completely unpreventable"
                        ]
                    ),
                    Question(
                        name="question3",
                        title="Do you typically receive advance notice about impending heatwaves",
                        type=QuestionType.RADIO,
                        required=True,
                        choices=[
                            "Always", "Often", "Sometimes", "Rarely", "Never"
                        ]
                    ),
                    Question(
                        name="question6",
                        title="(If Q5 = Always/Often/Sometimes) How do you receive heat warnings? (Multiple choice)",
                        type=QuestionType.CHECKBOX,
                        choices=[
                            "Weather app alerts",
                            "TV/radio news",
                            "Social media (WeChat, Weibo, etc.)",
                            "Government websites/official accounts",
                            "Newspapers",
                            "Family/friends/colleagues",
                            "Workplace/community notices"
                        ],
                    ),
                    Question(
                        name="question7",
                        title="What heat-avoidance behaviors do you adopt during heatwaves? (Multiple choice)",
                        type=QuestionType.CHECKBOX,
                        required=True,
                        choices=[
                            "Stay in air-conditioned spaces",
                            "Reduce outdoor activities",
                            "Seek shaded routes when outside",
                            "Wear light/loose/breathable clothing",
                            "Use sun protection (hats/glasses/umbrellas)",
                            "Increase water intake",
                            "Avoid strenuous outdoor work",
                            "Cool with water (showers/damp towels)",
                            "Use cooling products (menthol/ice pads)",
                            "Visit public cooling centers (libraries/shelters)",
                            "No specific actions"
                        ],
                    ),
                    Question(
                        name="question8",
                        title="How do your travel times change during heatwaves?",
                        type=QuestionType.RADIO,
                        required=True,
                        choices=[
                            "Significantly reduce all travel",
                            "Mainly reduce daytime travel (especially noon)",
                            "Reduce both daytime & evening travel",
                            "No significant change"
                        ],
                    ),
                    Question(
                        name="question9",
                        title="Preferred transportation during heatwaves? (Multiple choice)",
                        type=QuestionType.CHECKBOX,
                        required=True,
                        choices=[
                            "Private car/ride-hailing/taxi (AC)",
                            "Subway (AC)",
                            "Air-conditioned bus",
                            "Non-AC bus",
                            "Bicycle/e-bike (avoid peak heat)",
                            "Walking (avoid peak heat/shaded routes)"
                        ],
                    ),
                    Question(
                        name="question10",
                        title="Does your food intake change during heatwaves?",
                        type=QuestionType.RADIO,
                        required=True,
                        choices=[
                            "Significantly decreases",
                            "Slightly decreases",
                            "No change",
                            "Slightly increases",
                            "Significantly increases"
                        ]
                    ),
                    Question(
                        name="question11",
                        title="Do your food preferences change? (Multiple choice)",
                        type=QuestionType.CHECKBOX,
                        required=True,
                        choices=[
                            "Prefer lighter foods",
                            "Prefer cold dishes",
                            "Prefer spicy appetizers",
                            "Prefer soup-based foods",
                            "Prefer oily/hot foods",
                            "No significant change"
                        ],
                    ),
                    Question(
                        name="question12",
                        title="How is your sleep quality affected?",
                        type=QuestionType.RADIO,
                        required=True,
                        choices=[
                            "Very good (unaffected)",
                            "Fairly good (mildly affected)",
                            "Moderate (sleep difficulties)",
                            "Poor (frequent waking)",
                            "Very poor (severely disrupted)"
                        ]
                    ),
                    Question(
                        name="question13",
                        title="Does extreme heat affect your mood?",
                        type=QuestionType.RADIO,
                        required=True,
                        choices=[
                            "Much more irritable",
                            "Somewhat more irritable",
                            "More fatigued/lethargic",
                            "No significant change",
                            "Elevated mood"
                        ],
                    )
                ]
            )
        ]
    )
)

Survey2 = WorkflowStepConfig(
    type=WorkflowType.SURVEY,
    target_agent=[i for i in range(5, 105)],  # adjust this as needed
    survey=Survey(
        id=uuid4(),
        title="Mental Health survey",
        description="""
        The government is conducting a brief mental health survey.
        
        Please take a moment to reflect on your current mental and emotional state, and respond honestly to the following questions. Your answers will be kept confidential.
        
        Response in JSON format.
        """,
        created_at=datetime.datetime.now(),
        pages=[
            Page(
                name="page1",
                elements=[
                    Question(
                        type=QuestionType.RATING,
                        name="question4",
                        title="I get a lot of headaches, stomach-aches or sickness",
                        min_rating=1,
                        max_rating=3,
                        required=False,
                        choices=["0", "1", "2"]
                    ),
                    Question(
                        type=QuestionType.RATING,
                        name="question1",
                        title="I worry a lot",
                        min_rating=1,
                        max_rating=3,
                        required=False,
                        choices=["0", "1", "2"]
                    ),
                    Question(
                        type=QuestionType.RATING,
                        name="question2",
                        title="I am often unhappy, depressed or tearful",
                        min_rating=1,
                        max_rating=3,
                        required=False,
                        choices=["0", "1", "2"]
                    ),
                    Question(
                        type=QuestionType.RATING,
                        name="question3",
                        title="I am nervous in new situations. I easily lose confidence",
                        min_rating=1,
                        max_rating=3,
                        required=False,
                        choices=["0", "1", "2"]
                    ),
                    Question(
                        type=QuestionType.RATING,
                        name="question5",
                        title="I have many fears, I am easily scared",
                        min_rating=1,
                        max_rating=3,
                        required=False,
                        choices=["0", "1", "2"]
                    ),
                    Question(
                        type=QuestionType.RATING,
                        name="question6",
                        title="I get very angry and often lose my temper",
                        min_rating=1,
                        max_rating=3,
                        required=False,
                        choices=["0", "1", "2"]
                    ),
                    Question(
                        type=QuestionType.RATING,
                        name="question7",
                        title="I take things that are not mine from home, work or elsewhere",
                        min_rating=1,
                        max_rating=3,
                        required=False,
                        choices=["0", "1", "2"]
                    ),
                    Question(
                        type=QuestionType.RATING,
                        name="question8",
                        title="I fight a lot. I can make other people do what I want",
                        min_rating=1,
                        max_rating=3,
                        required=False,
                        choices=["0", "1", "2"]
                    ),
                    Question(
                        type=QuestionType.RATING,
                        name="question9",
                        title="I am often accused of lying or cheating",
                        min_rating=1,
                        max_rating=3,
                        required=False,
                        choices=["0", "1", "2"]
                    ),
                    Question(
                        type=QuestionType.RATING,
                        name="question10",
                        title="I am generally willing to do what other people want",
                        min_rating=1,
                        max_rating=3,
                        required=False,
                        choices=["0", "1", "2"]
                    ),
                    Question(
                        type=QuestionType.RATING,
                        name="question11",
                        title="I am restless, I find it hard to sit down for long",
                        min_rating=1,
                        max_rating=3,
                        required=False,
                        choices=["0", "1", "2"]
                    ),
                    Question(
                        type=QuestionType.RATING,
                        name="question12",
                        title="I am constantly fidgeting or squirming",
                        min_rating=1,
                        max_rating=3,
                        required=False,
                        choices=["0", "1", "2"]
                    ),
                    Question(
                        type=QuestionType.RATING,
                        name="question13",
                        title="I am easily distracted, I find it difficult to concentrate",
                        min_rating=1,
                        max_rating=3,
                        required=False,
                        choices=["0", "1", "2"]
                    ),
                    Question(
                        type=QuestionType.RATING,
                        name="question14",
                        title="I finish the work I'm doing. My attention is good",
                        min_rating=1,
                        max_rating=3,
                        required=False,
                        choices=["0", "1", "2"]
                    ),
                    Question(
                        type=QuestionType.RATING,
                        name="question15",
                        title="How often do you feel lonely (1. Often or always 5. Never)",
                        min_rating=1,
                        max_rating=5,
                        required=False,
                        choices=["1", "2", "3", "4", "5"]
                    ),
                    Question(
                        type=QuestionType.RATING,
                        name="question16",
                        title="I’ve been feeling optimistic about the future (1. None of the time  5. All of the time)",
                        min_rating=1,
                        max_rating=5,
                        required=False,
                        choices=["1", "2", "3", "4", "5"]
                    ),
                    Question(
                        type=QuestionType.RATING,
                        name="question17",
                        title="I’ve been feeling useful  (1. None of the time  5. All of the time)",
                        min_rating=1,
                        max_rating=5,
                        required=False,
                        choices=["1", "2", "3", "4", "5"]
                    ),
                    Question(
                        type=QuestionType.RATING,
                        name="question18",
                        title="I’ve been feeling relaxed   (1. None of the time  5. All of the time)",
                        min_rating=1,
                        max_rating=5,
                        required=False,
                        choices=["1", "2", "3", "4", "5"]
                    ),
                    Question(
                        type=QuestionType.RATING,
                        name="question19",
                        title="I’ve been dealing with problems well    (1. None of the time  5. All of the time)",
                        min_rating=1,
                        max_rating=5,
                        required=False,
                        choices=["1", "2", "3", "4", "5"]
                    ),
                    Question(
                        type=QuestionType.RATING,
                        name="question20",
                        title="I’ve been thinking clearly     (1. None of the time  5. All of the time)",
                        min_rating=1,
                        max_rating=5,
                        required=False,
                        choices=["1", "2", "3", "4", "5"]
                    ),
                    Question(
                        type=QuestionType.RATING,
                        name="question21",
                        title="I’ve been feeling close to other people    (1. None of the time  5. All of the time)",
                        min_rating=1,
                        max_rating=5,
                        required=False,
                        choices=["1", "2", "3", "4", "5"]
                    ),
                    Question(
                        type=QuestionType.RATING,
                        name="question22",
                        title="I’ve been able to make up my own mind about things   (1. None of the time  5. All of the time)",
                        min_rating=1,
                        max_rating=5,
                        required=False,
                        choices=["1", "2", "3", "4", "5"]
                    ),
                ]
            )
        ]
    )
)

Broadcast1 = WorkflowStepConfig(
    type=WorkflowType.MESSAGE_INTERVENE,
    target_agent=[i for i in range(5, 105)],  # adjust this as needed

    intervene_message="""
    Red Heatwave Warning Issued by New York City Meteorological Observatory
    
    Due to the influence of the subtropical high-pressure system, temperatures in all subdistricts of the main urban area are expected to reach around 40°C (104°F) today. Please take appropriate precautions to stay cool and prevent heat-related illnesses.
    
    Protective Guidelines:
    Relevant departments and organizations should implement emergency heat prevention measures in accordance with their responsibilities.
    All outdoor work under direct sunlight should be suspended, except for essential sectors.
    Protective measures must be taken for the elderly, the infirm, the sick, and young children.
    Relevant authorities must also pay close attention to fire prevention.
    """
)

Broadcast2 = WorkflowStepConfig(
    type=WorkflowType.MESSAGE_INTERVENE,
    target_agent=[i for i in range(5, 105)],  # adjust this as needed

    intervene_message="""
    Heatwave Has Subsided – Weather Returns to Normal — New York City
    
    New York City Meteorological Observatory Lifts Red Heatwave Warning
    
    The recent period of extreme high temperatures has ended. Temperatures across the city have returned to normal levels, with daytime highs expected to remain between 30–33°C (86–91°F) in the coming days.
    Residents may resume normal outdoor activities, but should remain aware of any delayed health effects from the earlier heatwave, especially among the elderly and those with pre-existing medical conditions.
    The Municipal Emergency Management Office thanks all citizens for their cooperation during the heat prevention period and reminds everyone to continue staying hydrated and maintaining basic health precautions.
    """
)
