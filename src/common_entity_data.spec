/* -*- c -*- */

  #include "spec.h"
  //Dwg_Object_Entity* _obj = ent;

  {
    // unsigned long pos = bit_position(dat);
    FIELD_B (preview_exists, 0);
    if (ent->preview_exists)
      {
#ifndef IS_JSON
        VERSIONS (R_13, R_2007)
          {
            // or DXF 92 for all PROXY vector preview data with classes
            FIELD_CAST (preview_size, RL, BLL, 160);
          }
        SINCE (R_2010)
          {
            FIELD_BLL (preview_size, 160);
          }
#endif
        if ((int)ent->preview_size >= 0 && ent->preview_size < 210210)
          {
            FIELD_BINARY (preview, ent->preview_size, 310);
          }
#ifndef IS_FREE
        else
          {
            LOG_ERROR ("Invalid preview_size: %lu kB",
                      (unsigned long)(ent->preview_size / 1000));
            //bit_set_position(dat, pos+1);
            error |= DWG_ERR_VALUEOUTOFBOUNDS;
          }
#endif
      }
  }

  VERSIONS (R_13, R_14)
    {
#ifdef IS_DECODER
      obj->bitsize = bit_read_RL (dat); // until the handles
#endif
#ifdef IS_ENCODER
      bit_write_RL (dat, obj->bitsize);
#endif
#ifndef IS_FREE
      LOG_TRACE ("bitsize: " FORMAT_BL " @%lu.%u\n", obj->bitsize,
                dat->byte - 4, dat->bit)
#endif
#ifdef IS_DECODER
    if (obj->bitsize > obj->size * 8)
      {
        LOG_ERROR ("Invalid bitsize " FORMAT_RL " => " FORMAT_RL, obj->bitsize,
                   obj->size * 8);
        obj->bitsize = obj->size * 8;
        error |= DWG_ERR_VALUEOUTOFBOUNDS;
      }
    else
      error |= obj_handle_stream (dat, obj, hdl_dat);
#endif
    }

  // TODO: r13-r14: 6B flags + 6B common params
  FIELD_BB (entmode, 0);
  // TODO: 2 more BB's
  FIELD_BL (num_reactors, 0); //ODA bug: BB as BS

  VERSIONS (R_13, R_14) //ODA bug
    {
      FIELD_B (isbylayerlt, 0);
      if (FIELD_VALUE (isbylayerlt))
        FIELD_VALUE (ltype_flags) = FIELD_VALUE (isbylayerlt) ? 0 : 3;
    }
  SINCE (R_2004) //ODA bug
    {
      FIELD_B (xdic_missing_flag, 0);
    }
  PRE (R_2004) //ODA bug
    {
      FIELD_B (nolinks, 0)
    }
  SINCE (R_2013)
    {
      FIELD_B (has_ds_binary_data, 0)
    }

  // TODO:
  // group 92 proxydata_size
  // group 310 proxydata

  FIELD_ENC (color, 62, 420); // ODA BUG, documented as CMC(B)

  DXF {
    if (FIELD_VALUE (ltype_scale) != 1.0)
      FIELD_BD (ltype_scale, 48);
  } else {
    FIELD_BD (ltype_scale, 48);
  }
  SINCE (R_2000)
    {
      // 00 BYLAYER, 01 BYBLOCK, 10 CONTINUOUS, 11 ltype handle
      FIELD_BB (ltype_flags, 0);
      // 00 BYLAYER, 01 BYBLOCK, 10 CONTINUOUS, 11 plotstyle handle
      FIELD_BB (plotstyle_flags, 0);
    }
  SINCE (R_2007)
    {
      FIELD_BB (material_flags, 0); //if not BYLAYER 00: 347 material handle
      DXF {
        if (FIELD_VALUE (material_flags))
          FIELD_HANDLE (material, 0, 347)
      }
      FIELD_RC (shadow_flags, 284); /* r2007+: 0 both, 1 casts, 2, receives, 3 no */
    }
  SINCE (R_2010)
    {
      FIELD_B (has_full_visualstyle, 0); // DXF?
      FIELD_B (has_face_visualstyle, 0);
      FIELD_B (has_edge_visualstyle, 0);
    }

  DXF {
    if (FIELD_VALUE (invisible))
      FIELD_BS (invisible, 60);
  } else {
    FIELD_BS (invisible, 60); //bit 0: 0 visible, 1 invisible
  }

  SINCE (R_2000) {
    DXF {
      if (FIELD_VALUE (linewt) != 29) {
        int lw = dxf_cvt_lweight (FIELD_VALUE (linewt));
        KEY (linewt); VALUE_RC ((signed char)lw, 370);
      }
    } else {
      FIELD_RC (linewt, 370);
    }
  }

