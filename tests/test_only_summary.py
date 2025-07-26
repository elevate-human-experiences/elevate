# MIT License
#
# Copyright (c) 2025 elevate-human-experiences
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

"""Module to test the text summarization functionality of the OnlySummary class."""

import logging
from typing import Any

import pytest

from common import setup_logging
from elevate.only_summary import OnlySummary, SummaryConfig, SummaryInput


logger = setup_logging(logging.INFO)


@pytest.mark.asyncio  # type: ignore
async def test_team_meeting_preparation(settings: Any) -> None:
    """Test summarizing a long email thread for team meeting prep."""
    content = """
Subject: Q4 Marketing Campaign Results and Next Steps

Hi team,

I wanted to share the comprehensive results from our Q4 marketing campaign that just wrapped up.

Performance Overview:
Our digital advertising spend was $45,000 across Google Ads, Facebook, and LinkedIn. We generated 2,847 leads, which is a 23% increase from Q3. The cost per lead averaged $15.82, down from $19.20 last quarter. Conversion rate from lead to customer improved to 12.3%.

Channel Breakdown:
Google Ads performed exceptionally well with a 31% increase in qualified leads. Facebook saw steady growth at 18% increase, but LinkedIn underperformed expectations with only 8% growth despite increased spend.

Customer Feedback:
Survey responses show 87% satisfaction with our new video content series. Customers particularly appreciated the product demo videos and behind-the-scenes content. However, 34% mentioned they'd like more technical deep-dives.

Challenges:
We experienced some technical issues with our landing pages in early November that likely cost us around 200 leads. The mobile checkout process also needs optimization - we're seeing 40% cart abandonment on mobile vs 22% on desktop.

Next Quarter Focus:
For Q1 2024, I recommend increasing Google Ads budget by 25%, reallocating LinkedIn spend to TikTok testing, and prioritizing mobile UX improvements. We should also consider expanding the video content series based on positive feedback.

Let me know your thoughts before our Friday strategy meeting.

Best,
Sarah
"""
    config = SummaryConfig(model=settings.with_model)
    only_summary_instance = OnlySummary(config=config)
    input_data = SummaryInput(
        content=content,
        context="Need to prepare talking points for Friday's marketing strategy meeting",
        purpose="meeting",
        audience="team",
    )
    result = await only_summary_instance.summarize_and_convert_to_markdown(input_data)
    assert result.summary
    assert result.key_insights
    assert result.word_count > 0
    logger.debug("Meeting Prep Summary (%s):\n%s", settings.with_model, result.summary)


@pytest.mark.asyncio  # type: ignore
async def test_executive_briefing_summary(settings: Any) -> None:
    """Test creating an executive briefing from industry news."""
    news_text = """
Tech Industry Weekly Report - Week of January 15, 2024

Major AI Developments:
OpenAI announced GPT-5 will launch in Q2 2024 with enhanced reasoning capabilities and better factual accuracy. The model reportedly shows 40% improvement in coding tasks and 30% better performance on mathematical reasoning. Beta testing with enterprise customers begins in March.

Microsoft continues its AI integration push, announcing Copilot will be embedded in all Office 365 applications by summer 2024. Early adopters report 25% productivity gains in document creation and data analysis tasks. Pricing will increase by $10/month per user.

Market Impact:
AI chip demand continues surging. NVIDIA's data center revenue hit $18.4B last quarter, up 206% year-over-year. AMD is gaining market share with their MI300X chips, signing deals with Meta and Google. Intel struggles to compete, with their Gaudi chips capturing less than 2% market share.

Regulatory Environment:
The EU's AI Act officially takes effect February 1st, creating the world's first comprehensive AI regulation framework. Companies have 6 months to comply with high-risk AI system requirements. US Congress is considering similar legislation but progress remains slow.

Investment Trends:
AI startups raised $4.2B in January alone, with enterprise automation and healthcare applications seeing the highest interest. Notable funding rounds include Anthropic ($500M), Scale AI ($300M), and Hugging Face ($235M).

Challenges:
Talent shortage intensifies as demand for AI engineers grows 300% year-over-year. Average salaries for senior ML engineers now exceed $400K in major tech hubs. Companies are investing heavily in retraining programs and university partnerships.
    """
    config = SummaryConfig(model=settings.with_model)
    only_summary_instance = OnlySummary(config=config)
    input_data = SummaryInput(
        content=news_text,
        context="Weekly leadership team meeting to discuss strategic AI investments",
        purpose="executive briefing",
        audience="executives",
    )
    result = await only_summary_instance.summarize_and_convert_to_markdown(input_data)
    assert result.summary
    assert len(result.key_insights) > 0
    logger.debug("Executive Briefing Summary (%s):\n%s", settings.with_model, result.summary)


@pytest.mark.asyncio  # type: ignore
async def test_student_study_notes(settings: Any) -> None:
    """Test converting academic paper into study notes for exam prep."""
    research_text = """
Abstract: Machine Learning in Medical Diagnosis: A Comprehensive Review

Introduction:
Machine learning (ML) has revolutionized medical diagnosis by enabling automated analysis of medical images, patient data, and clinical patterns. This comprehensive review examines current applications, challenges, and future directions of ML in healthcare diagnostics.

Methodology:
We analyzed 847 peer-reviewed studies published between 2019-2024, focusing on ML applications in radiology, pathology, cardiology, and emergency medicine. Studies were categorized by ML technique (deep learning, ensemble methods, support vector machines) and diagnostic domain.

Key Findings:

1. Diagnostic Accuracy: Deep learning models achieved 94.2% accuracy in skin cancer detection, outperforming dermatologists (87.1%) in controlled studies. Convolutional neural networks showed 96.8% accuracy in diabetic retinopathy screening.

2. Implementation Challenges: Only 23% of ML diagnostic tools have achieved FDA approval. Major barriers include data privacy concerns, lack of standardized datasets, and integration with existing hospital systems.

3. Cost-Benefit Analysis: Hospitals using ML diagnostic tools reported 31% reduction in diagnostic time and 18% cost savings, primarily from reduced need for specialist consultations and faster treatment initiation.

4. Geographic Disparities: 78% of ML diagnostic research focuses on diseases prevalent in developed countries, with limited research on tropical diseases or conditions common in low-resource settings.

Limitations:
Our review was limited to English-language publications and may not capture all global perspectives. Additionally, many studies had small sample sizes or were conducted in controlled environments that may not reflect real-world clinical settings.

Conclusions:
ML shows tremendous promise for improving diagnostic accuracy and efficiency. However, successful implementation requires addressing regulatory hurdles, ensuring equitable access, and developing robust validation frameworks for clinical deployment.
    """
    config = SummaryConfig(model=settings.with_model)
    only_summary_instance = OnlySummary(config=config)
    input_data = SummaryInput(
        content=research_text,
        context="Preparing for my Medical Informatics final exam next week",
        purpose="study",
        audience="students",
    )
    result = await only_summary_instance.summarize_and_convert_to_markdown(input_data)
    assert result.summary
    assert "Machine Learning" in result.summary or "ML" in result.summary
    logger.debug("Study Notes Summary:\n%s", result.summary)


@pytest.mark.asyncio  # type: ignore
async def test_customer_support_training(settings: Any) -> None:
    """Test creating customer support training material from technical docs."""
    technical_manual_text = """
Troubleshooting Guide: CloudSync Enterprise File Sharing Platform

Chapter 7: Common Upload and Sync Issues

7.1 File Upload Failures
Symptom: Users report files failing to upload or getting stuck at various percentages.

Causes and Solutions:
- Network connectivity issues: Check user's internet connection stability. Files over 2GB require stable connection for minimum 10 minutes.
- File format restrictions: CloudSync blocks .exe, .bat, .scr files for security. Advise users to compress these in .zip format.
- Storage quota exceeded: Premium accounts have 1TB limit, Basic accounts 100GB. Direct users to Account Settings > Storage to check usage.
- Filename issues: Files with special characters (&, %, #, <, >) may fail. Recommend renaming files using only letters, numbers, hyphens, and underscores.

7.2 Sync Conflicts
Symptom: Multiple versions of same file appear with "_conflict" suffix.

Resolution Process:
1. Identify the authoritative version (usually most recent modification date)
2. Guide user to rename other versions with descriptive suffixes
3. Delete unwanted conflict files after confirmation
4. Restart CloudSync application to clear cache

7.3 Mobile App Sync Delays
Symptom: Changes made on mobile don't appear on desktop for 15+ minutes.

Troubleshooting Steps:
- Force close and restart mobile app
- Check if device is on WiFi (cellular sync is limited to files under 50MB)
- Verify Background App Refresh is enabled for CloudSync
- For iOS: Settings > CloudSync > Background App Refresh = ON
- For Android: Settings > Apps > CloudSync > Battery > Allow background activity

7.4 Shared Folder Permission Issues
Symptom: Team members can't access shared folders or receive "permission denied" errors.

Permission Levels:
- Viewer: Can only download and view files
- Editor: Can upload, edit, and delete files
- Manager: Can edit permissions and add/remove team members
- Owner: Full control including folder deletion

Resolution:
1. Verify user email matches exactly (case-sensitive)
2. Check if user accepted invitation email
3. Remove and re-add user if permissions seem corrupted
4. For enterprise accounts, verify user is in correct Active Directory group
    """
    config = SummaryConfig(model=settings.with_model)
    only_summary_instance = OnlySummary(config=config)
    input_data = SummaryInput(
        content=technical_manual_text,
        context="Training new customer support agents on common CloudSync issues",
        purpose="training",
        audience="support team",
    )
    result = await only_summary_instance.summarize_and_convert_to_markdown(input_data)
    assert result.summary
    assert "CloudSync" in result.summary
    logger.debug("Support Training Summary:\n%s", result.summary)


@pytest.mark.asyncio  # type: ignore
async def test_investor_presentation_prep(settings: Any) -> None:
    """Test preparing investor presentation slides from quarterly results."""
    business_report_text = """
DataFlow Inc. - Q3 2024 Financial Results

Executive Summary:
DataFlow Inc. delivered exceptional Q3 results, demonstrating strong execution across all business segments. Revenue grew 42% year-over-year to $287M, driven by enterprise customer expansion and successful product launches.

Financial Highlights:
- Total Revenue: $287M (vs $202M Q3 2023, +42%)
- Recurring Revenue: $234M (81% of total revenue)
- Gross Margin: 73% (improved from 68% last year)
- Net Income: $23M (vs $8M loss Q3 2023)
- Cash and Equivalents: $445M
- Customer Count: 12,847 (net addition of 1,203 customers)

Segment Performance:

Enterprise Solutions (+55% YoY):
Our flagship enterprise data analytics platform continued strong momentum with 847 new customer wins. Average contract value increased to $89K (up from $67K). Key wins included Fortune 500 companies in healthcare, finance, and manufacturing sectors.

Small/Medium Business (+31% YoY):
SMB segment benefited from our self-service platform launch in June. Monthly active users grew to 34,500. Average revenue per user increased 18% due to premium feature adoption.

Professional Services (+28% YoY):
Implementation and consulting services revenue reached $42M. Margin improvement to 45% reflects successful automation of routine implementation tasks.

Operational Metrics:
- Employee Count: 2,847 (hired 312 this quarter)
- R&D Investment: $67M (23% of revenue)
- Customer Satisfaction Score: 4.6/5.0
- Net Promoter Score: +67

Looking Forward:
Q4 guidance calls for revenue of $320-330M, representing 35-39% growth. We're investing in AI capabilities, international expansion, and customer success initiatives to maintain growth trajectory.

Risks and Challenges:
- Increased competition from cloud providers
- Talent acquisition costs rising 23% year-over-year
- Potential economic headwinds affecting customer spending
    """
    config = SummaryConfig(model=settings.with_model)
    only_summary_instance = OnlySummary(config=config)
    input_data = SummaryInput(
        content=business_report_text,
        context="Creating slides for investor call next Tuesday - need key metrics and growth story",
        purpose="presentation",
        audience="investors",
    )
    result = await only_summary_instance.summarize_and_convert_to_markdown(input_data)
    assert result.summary
    assert "$287M" in result.summary or "287M" in result.summary
    logger.debug("Investor Presentation Summary:\n%s", result.summary)


@pytest.mark.asyncio  # type: ignore
async def test_contract_review_for_business_team(settings: Any) -> None:
    """Test summarizing legal contract for business stakeholder review."""
    legal_document_text = """
Software License and Services Agreement
Between: TechCorp Solutions LLC ("Provider") and MegaRetail Inc. ("Client")
Effective Date: February 1, 2024
Term: 3 years with automatic renewal

SOFTWARE LICENSE TERMS:

License Grant: Provider grants Client a non-exclusive, non-transferable license to use the TechCorp Inventory Management Suite ("Software") for internal business operations across up to 500 retail locations.

Usage Restrictions:
- Software may not be resold, sublicensed, or distributed to third parties
- Client may not reverse engineer, decompile, or create derivative works
- Maximum of 2,500 concurrent users across all locations
- Data export limited to standard formats (CSV, XML, JSON)

FINANCIAL TERMS:

License Fees:
- Year 1: $485,000 (paid quarterly at $121,250)
- Year 2: $509,250 (5% increase)
- Year 3: $534,713 (5% increase)
- Implementation fee: $125,000 (one-time)

Support and Maintenance: 20% of annual license fee
- 24/7 technical support with 2-hour response time
- Quarterly software updates and security patches
- Access to online training portal and documentation

SERVICE LEVEL COMMITMENTS:

Uptime Guarantee: 99.5% monthly uptime
- Penalties: 5% monthly fee credit for each 0.1% below 99.5%
- Scheduled maintenance windows: Maximum 4 hours monthly

Performance Standards:
- API response time: <200ms for 95% of requests
- Data processing: Real-time inventory updates within 30 seconds
- Report generation: Standard reports within 60 seconds

DATA AND SECURITY:

Data Ownership: Client retains full ownership of all data entered into Software

Security Measures:
- SOC 2 Type II compliance required
- Data encryption in transit (TLS 1.3) and at rest (AES-256)
- Annual third-party security audits
- GDPR and CCPA compliance for customer data

Data Backup: Provider maintains 3 backup copies with 30-day retention

TERMINATION CLAUSES:

Termination for Cause:
- Material breach with 30-day cure period
- Bankruptcy or insolvency of either party
- Failure to pay fees after 60-day notice

Termination for Convenience:
- Either party with 180-day written notice
- Client responsible for fees through end of current term

Data Transition: 90-day period for Client to export data after termination

DISPUTE RESOLUTION:

Governing Law: Delaware state law
Dispute Process:
1. Good faith negotiation (30 days)
2. Mediation with mutually agreed mediator (60 days)
3. Binding arbitration under AAA Commercial Rules

LIMITATIONS OF LIABILITY:

Provider's total liability limited to 12 months of license fees paid
Exclusions: No liability for consequential, indirect, or punitive damages
Exceptions: Unlimited liability for IP infringement, data breaches, or gross negligence
    """
    config = SummaryConfig(model=settings.with_model)
    only_summary_instance = OnlySummary(config=config)
    input_data = SummaryInput(
        content=legal_document_text,
        context="Business review meeting to decide if we should sign this vendor contract",
        purpose="business decision",
        audience="executives",
    )
    result = await only_summary_instance.summarize_and_convert_to_markdown(input_data)
    assert result.summary
    assert "$485,000" in result.summary or "485,000" in result.summary or "485K" in result.summary
    logger.debug("Contract Review Summary:\n%s", result.summary)


@pytest.mark.asyncio  # type: ignore
async def test_social_media_content_creation(settings: Any) -> None:
    """Test creating social media posts from longer content."""
    blog_post_text = """
The Ultimate Guide to Remote Work Productivity: Lessons from 50+ Digital Nomads

Introduction:
After interviewing 57 successful digital nomads across 23 countries, I've discovered the productivity secrets that separate thriving remote workers from those who struggle. Whether you're new to remote work or looking to optimize your current setup, these insights will transform how you approach location-independent productivity.

The Foundation: Environment Design

The most successful remote workers I interviewed all emphasized the critical importance of intentional environment design. Sarah Chen, a software architect who's worked from 15 countries, told me: "Your environment either supports your productivity or sabotages it. There's no neutral."

Key Environment Principles:
1. Lighting Matters More Than You Think: 89% of high-performers work near natural light sources. When that's not possible, they invest in full-spectrum LED lights that mimic natural daylight.

2. The 2-Meter Rule: Keep everything you need for work within 2 meters of your workspace. This includes water, snacks, notebooks, chargers, and backup equipment.

3. Noise Control: 67% use noise-canceling headphones even in quiet environments. The psychological effect of "switching on" work mode is as important as blocking distractions.

Time Management Strategies That Actually Work:

The Pomodoro Technique variations were popular, but the most effective approach was the "Energy-Based Scheduling" method used by top performers:

- Track your energy levels for one week
- Schedule your most important work during natural energy peaks
- Use low-energy periods for administrative tasks
- Take breaks before you feel tired, not after

Marcus Rodriguez, a marketing consultant earning $200K+ annually, shared: "I discovered I'm most creative between 6-9 AM and 3-5 PM. I guard those hours fiercely and schedule all my strategic work then."

Communication and Collaboration:

Successful remote workers are intentionally over-communicators. They've developed systems to stay connected with teams despite time zones and physical distance:

- Weekly "work personality" updates sharing current location, timezone, and working style
- Async video updates instead of status reports
- "Open door" virtual hours where colleagues can drop in
- Detailed handoff documents for time-zone coverage

Technology Stack Essentials:

While tools vary by profession, certain patterns emerged:

Core Infrastructure:
- Reliable internet with backup (mobile hotspot minimum)
- Cloud-based everything (files, passwords, applications)
- VPN for security and accessing geo-restricted content
- Time-tracking software (even if not required)

Productivity Tools That Made the Biggest Difference:
- Notion or Obsidian for knowledge management
- Calendly for scheduling across time zones
- Loom for async video communication
- Focus apps (Freedom, Cold Turkey, or Forest)

The Biggest Challenges and How to Overcome Them:

1. Loneliness and Isolation
Solution: Join co-working spaces or work from cafes 2-3 times per week. Many nomads also join local sports teams or hobby groups.

2. Time Zone Juggling
Solution: Use scheduling tools that show multiple time zones and always confirm meeting times in the other person's timezone.

3. Inconsistent Internet
Solution: Always have 2-3 backup options (mobile hotspot, nearby cafe, co-working space) and test them before you need them.

Final Thoughts:

The most successful remote workers treat productivity as a skill to be developed, not a personality trait. They experiment, measure results, and continuously optimize their systems. As digital nomad and productivity coach Jessica Park told me: "Productivity isn't about working harder - it's about creating systems that make the right work effortless."
    """
    config = SummaryConfig(model=settings.with_model)
    only_summary_instance = OnlySummary(config=config)
    input_data = SummaryInput(
        content=blog_post_text,
        context="Creating LinkedIn post to promote this blog article to my professional network",
        purpose="social media",
        audience="professionals",
    )
    result = await only_summary_instance.summarize_and_convert_to_markdown(input_data)
    assert result.summary
    assert "remote work" in result.summary.lower() or "productivity" in result.summary.lower()
    logger.debug("Social Media Summary:\n%s", result.summary)


@pytest.mark.asyncio  # type: ignore
async def test_book_club_discussion_prep(settings: Any) -> None:
    """Test creating discussion points from book chapter for book club meeting."""
    fiction_excerpt_text = """
Chapter 12: The Weight of Choices
From "The Archivist's Daughter" by Maria Santos

Lila stared at the ancient leather journal in her hands, its pages yellowed with age and secrets. Three weeks had passed since she'd discovered it hidden in her grandmother's attic, and every night since then had been filled with dreams of places she'd never seen and people she'd never met.

The journal belonged to her great-great-grandmother, Elena Vasquez, who had disappeared in 1943 during the Spanish Civil War. Family legend claimed she'd been killed by Franco's forces, but the journal told a different story—one of underground resistance networks, secret codes, and a love affair that could have changed the course of history.

As Lila translated each entry, she realized the journal wasn't just a historical record. It was a roadmap. Elena had hidden something—something valuable enough that people had died protecting its location. And now, somehow, that burden had fallen to Lila.

The weight of the decision pressed down on her shoulders as she sat in her small Barcelona apartment, looking out at the same streets her ancestor had once walked. Should she follow the clues and risk everything to uncover Elena's secret? Or should she destroy the journal and let the past stay buried?

Her phone buzzed with a text from Dr. Martinez, the history professor who'd been helping her translate the more obscure passages: "Found something interesting about the church Elena mentions. Can we meet tomorrow?"

Lila's heart raced. Each new discovery made turning back more impossible, yet the danger felt increasingly real. Yesterday, she'd noticed the same man in the gray coat outside her apartment three times. Paranoia, she'd told herself, but Elena's words echoed in her mind: "Trust no one, especially those who claim to help."

The journal lay open to Elena's final entry, dated just days before her disappearance:

"If anyone finds this, know that some secrets are worth dying for, but none are worth living with alone. The choice I make tomorrow will echo through generations. I pray my family will understand that sometimes, love requires the ultimate sacrifice."

Lila closed the journal and walked to her window. The streetlights blurred through her tears as she realized she already knew what she had to do. Elena's story deserved to be told, and the secret she'd died protecting deserved to see daylight.

But first, she had to survive long enough to tell it.
    """
    config = SummaryConfig(model=settings.with_model)
    only_summary_instance = OnlySummary(config=config)
    input_data = SummaryInput(
        content=fiction_excerpt_text,
        context="Our book club is discussing this chapter next Thursday and I want to prepare good discussion questions",
        purpose="discussion prep",
        audience="book club members",
    )
    result = await only_summary_instance.summarize_and_convert_to_markdown(input_data)
    assert result.summary
    assert "Lila" in result.summary or "Elena" in result.summary
    logger.debug("Book Club Discussion Summary:\n%s", result.summary)
