pub enum Daytime {
    Sunrise,
    Morning,
    Noon,
    Afternoon,
    Sunset,
    EarlyNight,
    Midnight,
    LateNight,
}

pub enum Day {
    Monday,
    Tuesday,
    Wednesday,
    Thursday,
    Friday,
    Saturday,
    Sunday,
}

pub struct Date {
    day: u8,
    month: u8,
}

pub enum MoonPhase {
    NewMoon,
    RisingMoon,
    FullMoon,
    DecreasingMoon,
}