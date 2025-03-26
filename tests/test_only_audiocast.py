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
    audiocast.cast(content, audio_out_path="~/Downloads/")


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
