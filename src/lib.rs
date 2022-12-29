pub mod tags;
pub mod time;

pub struct Rule {
    pkmn: u16,
    weight: f32,

    /// "Anded" locations i.e. `lake, mountain` would mean a like on a mountain
    location: Vec<tags::Tag>,

    time: time::Time,
}

pub fn rules() -> Vec<Rule> {
    use tags::*;
    use time::*;
    vec![
        Rule {
            pkmn: 1,
            weight: 1.0,
            location: vec![Tag::Amenity(Amenity::Bench), Tag::Landuse(Landuse::Residential)],
            time: Time {
                daytime: Some(Daytime::Noon),
                day: Some(Day::Sunday),
                date: None,
                moon_phase: None,
            },
        }
    ]
}