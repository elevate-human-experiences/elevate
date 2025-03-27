import os
from elevate.only_audiocast import (
    OnlyAudiocast,
    CastConfiguration,
    SpeakerConfig,
    ListenerConfig,
)


def test_create_default_audiocast() -> None:
    content = (
        "San Francisco is a city in California. It is known for the Golden Gate Bridge."
    )
    audiocast = OnlyAudiocast()
    audiocast.cast(
        content,
        audio_out_path=f"{os.environ['HOME']}/Downloads/",
    )


def test_create_two_people_podcast() -> None:
    content = """The standard cosmological model rests on a foundational assumption: that the universe is homogeneous and isotropic on large scales. However, this assumption has long been questioned due to observable evidence of substantial cosmic inhomogeneities—galaxy clusters, vast voids, and filamentary structures spanning billions of light-years. Such uneven distributions of matter challenge the premise that the universe expands uniformly. Post-doctorate astrophysics researchers are increasingly examining the implications of these structures, realizing that overlooking them might significantly distort our understanding of cosmic expansion.

One emerging theory gaining traction is timescape cosmology, which offers a compelling alternative to the elusive concept of dark energy. Timescape theory posits that different regions of the universe experience their own distinct "timescapes"—unique expansion histories shaped by local gravitational environments. In this model, what appears to be an accelerating universe (currently explained by invoking dark energy) is instead interpreted as an observational artifact arising from comparing clocks and rulers in regions with varying gravitational conditions. Essentially, the accelerated expansion emerges naturally from general relativity when accounting properly for gravitational inhomogeneities, eliminating the need for mysterious forms of energy.

This theory is resonating within the astrophysics community largely because of its elegant explanatory power and reduction in speculative components. Timescape cosmology aligns closely with recent astronomical observations highlighting significant cosmic structures, offering an interpretation firmly grounded in established physics rather than unknown entities. As post-doc students delve deeper into the precision cosmology era, leveraging data from advanced telescopes and gravitational-wave observatories, exploring and refining timescape models becomes a promising frontier—one that may reshape our fundamental understanding of the universe and its evolution."""

    cast_configuration = CastConfiguration(
        speakers=[
            SpeakerConfig(
                name="Professor Mitchell",
                background="Expert in astrophysics focusing on gravitational inhomogeneities",
                expertise="high",
                speaking_style="interview",
                level_of_expertise="post-doc",
                focus_aspect="timescape cosmology",
                depth="high",
            ),
            SpeakerConfig(
                name="Professor Carter",
                background="Renowned cosmologist with extensive research in timescape theory",
                expertise="high",
                speaking_style="conversational",
                level_of_expertise="post-doc",
                focus_aspect="observational cosmology",
                depth="high",
            ),
        ],
        listener=ListenerConfig(
            expertise="advanced",
            summary_of_similar_content=["Post-doctoral astrophysics discussions"],
            level_of_expertise="high",
            depth="high",
        ),
    )

    audiocast = OnlyAudiocast()
    audiocast.cast(
        content,
        cast_configuration=cast_configuration,
        audio_out_path=f"{os.environ['HOME']}/Downloads/",
    )


def test_create_art_teacher_conversation() -> None:
    content = """Impressionism was a revolutionary art movement originating in France in the late 19th century. Impressionist painters, such as Monet, Renoir, and Degas, focused on capturing the immediate impression of a scene, particularly the effects of light, color, and atmosphere. Instead of precise detail, their paintings were characterized by quick brushstrokes and vibrant colors, conveying mood and emotion rather than realistic accuracy.

An important hallmark of impressionism was painting en plein air, meaning outdoors. Artists abandoned studios to paint directly from nature, allowing them to observe and capture the changing qualities of light firsthand. This fresh perspective challenged traditional academic standards and faced initial resistance, eventually transforming public appreciation and paving the way for modern art."""

    cast_configuration = CastConfiguration(
        speakers=[
            SpeakerConfig(
                name="Ms. Lucy",
                background="High school art teacher passionate about art history",
                expertise="high",
                speaking_style="friendly, inspiring",
                level_of_expertise="art educator",
                focus_aspect="Impressionism’s visual techniques",
                depth="medium",
            ),
            SpeakerConfig(
                name="Alex",
                background="Curious student interested in painting",
                expertise="novice",
                speaking_style="curious, enthusiastic",
                level_of_expertise="high school student",
                focus_aspect="Student perspectives and questions",
                depth="medium",
            ),
        ],
        listener=ListenerConfig(
            expertise="beginner",
            summary_of_similar_content=["basic art movements overview"],
            level_of_expertise="high school student",
            depth="low",
        ),
    )

    audiocast = OnlyAudiocast()
    audiocast.cast(
        content,
        cast_configuration=cast_configuration,
        audio_out_path=f"{os.environ['HOME']}/Downloads/",
    )


def test_create_children_storytelling_session() -> None:
    content = """In the magical kingdom of Eldoria lived a brave little fox named Finley. Unlike other foxes, Finley dreamed of flying. Each evening, Finley climbed the tallest oak and gazed at the stars, whispering a wish to soar among them. One night, a wise old owl named Orion overheard Finley's wish and decided to help.

With the owl’s guidance, Finley set off on a journey through enchanted forests and shimmering lakes to find the legendary Wings of Eldoria. Along the way, Finley faced challenges and made many animal friends who offered their help. Together, they discovered courage, friendship, and that true magic comes from believing in yourself."""

    cast_configuration = CastConfiguration(
        speakers=[
            SpeakerConfig(
                name="Narrator",
                background="Experienced children's storyteller",
                expertise="high",
                speaking_style="animated, expressive, multiple character voices",
                level_of_expertise="professional storyteller",
                focus_aspect="Engaging young audience through expressive narration",
                depth="light",
            )
        ],
        listener=ListenerConfig(
            expertise="beginner",
            summary_of_similar_content=["Classic fairytales", "Animal stories"],
            level_of_expertise="children",
            depth="light",
        ),
    )

    audiocast = OnlyAudiocast()
    audiocast.cast(
        content,
        cast_configuration=cast_configuration,
        audio_out_path=f"{os.environ['HOME']}/Downloads/",
    )
