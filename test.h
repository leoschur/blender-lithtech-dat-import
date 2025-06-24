// runtime/world/src/de_world.h Surface flags.
#define SURF_SOLID              (1<<0)      // Solid.
#define SURF_NONEXISTENT        (1<<1)      // Gets removed in preprocessor.
#define SURF_INVISIBLE          (1<<2)      // Don't draw.
#define SURF_TRANSPARENT        (1<<3)      // Translucent.
#define SURF_SKY                (1<<4)      // Sky portal.
#define SURF_BRIGHT             (1<<5)      // Fully bright.
#define SURF_FLATSHADE          (1<<6)      // Flat shade this poly.
#define SURF_LIGHTMAP           (1<<7)      // Lightmap this poly.
#define SURF_NOSUBDIV           (1<<8)      // Don't subdivide the poly.
#define SURF_HULLMAKER          (1<<9)      // Adds hulls to make PVS better for open areas.
#define SURF_PARTICLEBLOCKER	(1<<10)		// A poly used to block particle movement
#define SURF_DIRECTIONALLIGHT   (1<<11)     // This surface is only lit by the GlobalDirLight.
#define SURF_GOURAUDSHADE       (1<<12)     // Gouraud shade this poly.
#define SURF_PORTAL             (1<<13)     // This surface defines a portal that can be opened/closed.
#define SURF_PANNINGSKY         (1<<15)     // This surface has the panning sky overlaid on it.

#define SURF_PHYSICSBLOCKER     (1<<17)     // A poly used to block player movement
#define SURF_TERRAINOCCLUDER    (1<<18)     // Used for visibility calculations on terrain.
#define SURF_ADDITIVE           (1<<19)     // Add source and dest colors.

#define SURF_VISBLOCKER         (1<<21)     // Blocks off the visibility tree
#define SURF_NOTASTEP           (1<<22)     // Don't try to step up onto this polygon
#define SURF_MIRROR             (1<<23)     // This surface is a mirror

// tools/shared/engine/de_world.h Surface flags.
#define SURF_SOLID				(1<<0)		// Solid.
#define SURF_NONEXISTENT		(1<<1)		// Gets removed in preprocessor.
#define SURF_INVISIBLE			(1<<2)		// Don't draw.

#define SURF_SKY				(1<<4)		// Sky portal.

#define SURF_FLATSHADE			(1<<6)		// Flat shade this poly.
#define SURF_LIGHTMAP			(1<<7)		// Lightmap this poly.
#define SURF_NOSUBDIV			(1<<8)		// Don't subdivide the poly.

#define SURF_PARTICLEBLOCKER	(1<<10)		// A poly used to block particle movement

#define SURF_GOURAUDSHADE		(1<<12)		// Gouraud shade this poly.




#define SURF_PHYSICSBLOCKER     (1<<17)     // A poly used to block player movement

#define SURF_RBSPLITTER			(1<<19)		// Split renderblocks with this polygon

#define SURF_VISBLOCKER			(1<<21)		// Blocks off the visibility tree
#define SURF_NOTASTEP			(1<<22)		// Don't try to step up onto this polygon

#define SURF_RECEIVELIGHT		(1<<24)		// Receives light (otherwise it is just the local ambient)
#define SURF_RECEIVESHADOWS		(1<<25)		// Shadows are cast onto this surface
#define SURF_RECEIVESUNLIGHT	(1<<26)		// Should sunlight affect this polygon

#define SURF_SHADOWMESH			(1<<28)		// Receives shadow meshing
#define SURF_CASTSHADOWMESH		(1<<29)		// Casts shadow mesh shadows
#define SURF_CLIPLIGHT			(1<<30)		// Clips light (casts shadows)