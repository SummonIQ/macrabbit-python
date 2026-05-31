# Service database shared between TUI and GUI
SERVICE_DATABASE = {
  # Accessibility
  "com.apple.accessibility.MotionTrackingAgent": {
    "description": "Related to accessibility features that involve motion tracking, such as Head Pointer.",
    "impact": "Disabling will prevent the use of accessibility features that rely on tracking user motion.",
  },
  "com.apple.accessibility.axassetsd": {
    "description": "Manages accessibility assets and resources used by various accessibility features.",
    "impact": "Accessibility features may function incorrectly or fail to load necessary resources.",
  },
  "com.apple.universalaccessd": {
    "description": "A core daemon for Universal Access, providing features for users with disabilities.",
    "impact": "Will likely break most accessibility features, such as VoiceOver, Zoom, and Switch Control.",
  },
  "com.apple.voicebankingd": {
    "description": "Manages the creation and use of personal voices for accessibility features like Personal Voice.",
    "impact": "You will not be able to create or use a Personal Voice for text-to-speech.",
  },
  "com.apple.AXMediaUtilitiesService": {
    "description": "Provides accessibility services for media content, such as descriptions for the visually impaired.",
    "impact": "Media-related accessibility features may not function correctly.",
  },
  "com.apple.accessibility.mediaaccessibilityd": {
    "description": "Daemon for Media Accessibility, providing features like subtitles, captions, and audio descriptions.",
    "impact": "Subtitles, closed captions, and other media-related accessibility features may not work.",
  },
  "com.apple.accessibility.heard": {
    "description": "Part of the 'Sound Recognition' accessibility feature, which listens for specific sounds and notifies the user.",
    "impact": "The 'Sound Recognition' feature will not function.",
  },
  "com.apple.universalaccessAuthWarn": {
    "description": "Shows an authentication warning related to Universal Access features.",
    "impact": "System warnings for accessibility features may not appear.",
  },
  "com.apple.accessibility.LiveTranscriptionAgent": {
    "description": "Manages the Live Transcription feature for audio.",
    "impact": "Live Transcription for audio content will not function.",
  },
  "com.apple.accessibility.AXVisualSupportAgent": {
    "description": "Provides visual support services for various accessibility features.",
    "impact": "Visual accessibility aids may not function correctly.",
  },
  "com.apple.universalaccesscontrol": {
    "description": "Daemon for managing Universal Access controls.",
    "impact": "Core accessibility control features will be disabled.",
  },
  "com.apple.AccessibilityUIServer": {
    "description": "User interface server for accessibility features.",
    "impact": "The UI components of accessibility features like VoiceOver or Zoom may not display correctly.",
  },
  "com.apple.DwellControl": {
    "description": "An accessibility feature allowing pointer control using head or eye tracking.",
    "impact": "Dwell Control functionality will be disabled.",
  },
  "com.apple.VoiceOver": {
    "description": "The core screen reader service for macOS.",
    "impact": "The VoiceOver screen reader will be completely disabled.",
  },
  "com.apple.ScreenReaderUIServer": {
    "description": "User interface server for the screen reader (VoiceOver).",
    "impact": "The visual interface for VoiceOver will not function.",
  },
  "com.apple.AssistiveControl": {
    "description": "Service for the Assistive Control feature, allowing use of adaptive accessories.",
    "impact": "Will disable the ability to use switch controls and other assistive devices.",
  },
  "com.apple.KeyboardAccessAgent": {
    "description": "Agent for Keyboard Access features, allowing full control of the UI from the keyboard.",
    "impact": "Full Keyboard Access and other keyboard-related accessibility features will not work.",
  },
  "com.apple.accessibility.dfrhud": {
    "description": "Manages the accessibility Heads-Up Display (HUD) for the Touch Bar (DFR).",
    "impact": "Accessibility features related to the Touch Bar will not work.",
  },
  # Advertising & Analytics
  "com.apple.ap.adprivacyd": {
    "description": "Part of Apple's advertising framework; manages ad privacy and tracking settings.",
    "impact": "May interfere with the system's ability to respect your ad tracking preferences.",
  },
  "com.apple.ap.promotedcontentd": {
    "description": "Fetches and displays promoted content within Apple's applications like the App Store.",
    "impact": "Will likely prevent the display of promoted or featured content in various Apple apps.",
  },
  "com.apple.adid": {
    "description": "Manages the advertising identifier (IDFA) used for tracking in apps.",
    "impact": "May affect ad tracking and personalization in apps.",
  },
  "com.apple.parsec-fbf": {
    "description": "Responsible for periodic flushing and uploading of Siri Search analytics data.",
    "impact": "Disabling this will stop the system from sending Siri Search analytics to Apple.",
  },
  "com.apple.analyticsd": {
    "description": "The main daemon for capturing and reporting diagnostic and usage data to Apple.",
    "impact": "No diagnostic or usage data will be sent to Apple. This may be desirable for privacy.",
  },
  "com.apple.osanalytics.osanalyticshelper": {
    "description": "A helper process for the analytics daemon, likely involved in gathering system-level logs.",
    "impact": "May prevent certain system-level diagnostic data from being collected.",
  },
  "com.apple.symptomsd": {
    "description": "Related to network diagnostics and analytics.",
    "impact": "May affect the system's ability to diagnose network issues.",
  },
  "com.apple.wifianalyticsd": {
    "description": "Daemon for collecting Wi-Fi diagnostics and analytics.",
    "impact": "No Wi-Fi analytics will be sent to Apple.",
  },
  "com.apple.audioanalyticsd": {
    "description": "Daemon for collecting audio system diagnostics and analytics.",
    "impact": "No audio-related analytics will be sent to Apple.",
  },
  "com.apple.ecosystemanalyticsd": {
    "description": "Analyzes interactions within the Apple device ecosystem for diagnostic purposes.",
    "impact": "No ecosystem-related analytics will be sent to Apple.",
  },
  "com.apple.perfpowermetricd": {
    "description": "Collects performance and power metrics for analytics.",
    "impact": "No performance and power analytics will be sent to Apple.",
  },
  "com.apple.metrickitd": {
    "description": "Gathers and reports aggregated performance and usage metrics from apps for developers.",
    "impact": "Developers will not receive MetricKit reports for their apps from your device.",
  },
  "com.apple.analyticsagent": {
    "description": "User-level agent for collecting and reporting diagnostic and usage data.",
    "impact": "No diagnostic or usage data from the user session will be sent to Apple.",
  },
  "com.apple.dprivacyd": {
    "description": "Daemon related to Differential Privacy, a technique for collecting anonymized usage data.",
    "impact": "The system will not contribute to Apple's differential privacy data sets.",
  },
  "com.apple.PerfPowerTelemetryClientRegistrationService": {
    "description": "A service for registering clients to receive performance and power telemetry data.",
    "impact": "The system and applications will not be able to collect performance and power usage data for analytics.",
  },
  "com.apple.memoryanalyticsd": {
    "description": "A daemon that collects analytics on memory usage.",
    "impact": "The system will not collect memory usage data for diagnostics and analytics.",
  },
  # App & Store Related
  "com.apple.appstoreagent": {
    "description": "An agent that supports the App Store, handling downloads, installations, and updates initiated by the user.",
    "impact": "The App Store may not be able to download, install, or update applications correctly.",
  },
  "com.apple.appstored": {
    "description": "The main daemon for the Mac App Store, handling background tasks related to app updates and licensing.",
    "impact": "Automatic app updates will not work, and there may be issues with purchased app validation.",
  },
  "com.apple.commerce": {
    "description": "A core agent for handling App Store transactions, in-app purchases, and license validation.",
    "impact": "CRITICAL: The App Store will not function. You will not be able to purchase, update, or restore apps.",
  },
  "com.apple.passd": {
    "description": "A daemon that manages passes in Wallet and handles Apple Pay functionality.",
    "impact": "Apple Pay and Wallet functionality will not work.",
  },
  "com.apple.financed": {
    "description": "A background daemon for Apple Pay and Wallet services.",
    "impact": "Apple Pay and Wallet functionality, including managing cards and passes, will not work.",
  },
  "com.apple.watchlistd": {
    "description": "A support daemon for the Apple TV app, likely managing the 'Up Next' watchlist.",
    "impact": "The 'Up Next' feature in the TV app may not sync or update correctly.",
  },
  "com.apple.triald.system": {
    "description": "Manages trial periods for applications from the Mac App Store.",
    "impact": "App trials may not function correctly or their status may not be tracked.",
  },
  "com.apple.newsd": {
    "description": "Daemon for the Apple News service.",
    "impact": "Apple News content and widgets will not update.",
  },
  "com.apple.appinstalld": {
    "description": "Handles requests for app installation.",
    "impact": "Apps may fail to install correctly.",
  },
  "com.apple.assetsubscriptiond": {
    "description": "Manages subscriptions to content assets.",
    "impact": "Content subscriptions in apps like News or TV may not work.",
  },
  "com.apple.bookassetd": {
    "description": "Manages assets for the Books app.",
    "impact": "Books and audiobooks may not download or display correctly.",
  },
  "com.apple.storeaccountd": {
    "description": "Manages App Store account information.",
    "impact": "You may have issues signing into or managing your App Store account.",
  },
  "com.apple.storeuid": {
    "description": "Provides user interface elements for the App Store.",
    "impact": "App Store dialogs and notifications may not appear.",
  },
  "com.apple.storedownloadd": {
    "description": "Manages downloads from the App Store.",
    "impact": "App downloads and updates may fail.",
  },
  "com.apple.appsleep": {
    "description": "Potentially related to managing the 'sleep' or suspended state of applications.",
    "impact": "Unknown, but could affect app lifecycle management.",
  },
  "com.apple.storekitagent": {
    "description": "Agent for StoreKit, handling in-app purchases and interactions with the App Store.",
    "impact": "In-app purchases will not work.",
  },
  "com.apple.appplaceholdersyncd": {
    "description": "Syncs app placeholders, likely for restoring apps on a new device.",
    "impact": "Setting up a new Mac from a backup might not correctly show all installing apps.",
  },
  "com.apple.askpermissiond": {
    "description": "Manages 'Ask to Buy' requests for Family Sharing.",
    "impact": "'Ask to Buy' notifications and purchase approvals will not function.",
  },
  "com.apple.amsondevicestoraged": {
    "description": "Apple Media Services on-device storage management.",
    "impact": "May affect how media and App Store data is stored and managed.",
  },
  "com.apple.amsaccountsd": {
    "description": "Manages accounts for Apple Media Services (App Store, Music, TV).",
    "impact": "Account-related features in media apps may fail.",
  },
  "com.apple.amsengagementd": {
    "description": "Handles user engagement features for Apple Media Services.",
    "impact": "Promotional content or user engagement prompts in media apps may not work.",
  },
  "com.apple.AppStoreDaemon.StorePrivilegedODRService": {
    "description": "Handles On-Demand Resources (ODR) for App Store applications, allowing apps to download content as needed.",
    "impact": "Apps that use On-Demand Resources may fail to download additional content, leading to incomplete functionality."
  },
  "com.apple.AppStoreDaemon.StorePrivilegedTaskService": {
    "description": "Performs privileged tasks for the App Store daemon, such as installations and updates that require higher permissions.",
    "impact": "The App Store may fail to install or update applications, particularly those requiring system-level changes."
  },
  "com.apple.eligibilityd": {
    "description": "A daemon that determines if the device is eligible for certain services or features.",
    "impact": "You may not be able to access certain Apple services if your device cannot be verified as eligible."
  },
  "com.apple.fairplayd": {
    "description": "The daemon for FairPlay, Apple's digital rights management (DRM) technology.",
    "impact": "You will not be able to play DRM-protected content from the iTunes Store or Apple Music."
  },
  "com.apple.fairplaydeviceidentityd": {
    "description": "A daemon that manages the device's identity for FairPlay DRM.",
    "impact": "Similar to `fairplayd`, this is critical for playing DRM-protected content."
  },
  "com.apple.storereceiptinstaller": {
    "description": "A tool that installs receipts for App Store purchases.",
    "impact": "The system may not correctly record the receipts for your purchased applications, potentially causing licensing issues."
  },
  # Touch Bar
  "com.apple.touchbarserver": {
    "description": "Manages the Touch Bar on MacBook Pro models that have one.",
    "impact": "The Touch Bar and Control Strip will become non-functional.",
  },
  "com.apple.controlstrip": {
    "description": "The process that manages the Control Strip on the Touch Bar.",
    "impact": "The Control Strip on the Touch Bar will be disabled.",
  },
  # Siri
  "com.apple.assistantd": {
    "description": "The main Siri daemon that handles voice commands and queries.",
    "impact": "Siri will not function at all.",
  },
  "com.apple.corespeechd": {
    "description": "Core speech recognition and synthesis daemon for Siri.",
    "impact": "Siri voice recognition and speech synthesis will not work.",
  },
  "com.apple.siriknowledged": {
    "description": "Siri's knowledge daemon that manages Siri's understanding and responses.",
    "impact": "Siri will not be able to understand or respond to queries.",
  },
  "com.apple.Siri.agent": {
    "description": "User-level Siri agent that provides the Siri interface.",
    "impact": "The Siri user interface will not be available.",
  },
  "com.apple.shazamd": {
    "description": "Shazam music recognition daemon.",
    "impact": "Shazam music recognition will not work.",
  },
  "com.apple.speech.speechsynthesisd": {
    "description": "Speech synthesis daemon for text-to-speech.",
    "impact": "Text-to-speech functionality will not work.",
  },
  "com.apple.speech.synthesisserver": {
    "description": "Speech synthesis server for system-wide text-to-speech.",
    "impact": "System-wide text-to-speech will not function.",
  },
  "com.apple.DictationIM": {
    "description": "Dictation input method for converting speech to text.",
    "impact": "Dictation (speech-to-text) will not work.",
  },
  "com.apple.corespeechd_system": {
    "description": "System-level speech recognition daemon.",
    "impact": "System-level speech recognition features will not work.",
  },
  "com.apple.siri.acousticsignature": {
    "description": "Siri's acoustic signature service for voice recognition.",
    "impact": "Siri's voice recognition accuracy may be reduced.",
  },
  "com.apple.assistant_service": {
    "description": "Assistant service for Siri functionality.",
    "impact": "Siri assistant features will not work.",
  },
  "com.apple.siriactionsd": {
    "description": "Siri actions daemon for handling Siri shortcuts and actions.",
    "impact": "Siri shortcuts and actions will not function.",
  },
  "com.apple.SiriTTSTrainingAgent": {
    "description": "Siri text-to-speech training agent.",
    "impact": "Siri's voice training features will not work.",
  },
  "com.apple.sirittsd": {
    "description": "Siri text-to-speech daemon.",
    "impact": "Siri's text-to-speech will not function.",
  },
  "com.apple.siri.context.service": {
    "description": "Siri context service for maintaining conversation context.",
    "impact": "Siri's conversation context and follow-up features will not work.",
  },
  "com.apple.speech.speechsynthesisd.x86_64": {
    "description": "x86_64 specific speech synthesis daemon.",
    "impact": "Speech synthesis on Intel Macs may not work properly.",
  },
  "com.apple.speech.speechdatainstallerd": {
    "description": "Speech data installer for downloading voice packages.",
    "impact": "Voice package downloads for speech synthesis will not work.",
  },
  "com.apple.SpeechRecognitionCore.brokerd": {
    "description": "Speech recognition broker daemon.",
    "impact": "Speech recognition services will not function.",
  },
} 